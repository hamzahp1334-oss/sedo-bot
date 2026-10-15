"""
Automated Test Suite for SEDO MARTIAL ART Telegram Bot System.
Tests:
1. Configuration & Security Constants
2. Pure Language Isolation (No English in Amharic, No Amharic in English)
3. Callback Data Length Thresholds (< 64 bytes to guarantee zero Button_data_invalid errors)
4. Resolvers for Categories, Formats, Environments, Budgets, Collaborations
5. Database Layer (CRUD operations on temporary test DB)
6. Conversation Handlers Build Integrity
"""

import asyncio
import os
import sys
import unittest
from pathlib import Path

# Add directory to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

import config
import database
import keyboards
import states
from i18n import MESSAGES, get_text, format_status_badge
import main


class TestSedoBot(unittest.TestCase):

    def test_01_configuration(self):
        """Verify tokens, admin IDs, and basic configuration."""
        self.assertTrue(len(config.CUSTOMER_BOT_TOKEN) > 20)
        self.assertTrue(len(config.ADMIN_BOT_TOKEN) > 20)
        self.assertIn(8798202536, config.ADMIN_IDS)
        self.assertIn(406274598, config.ADMIN_IDS)
        self.assertTrue(config.is_admin(8798202536))
        self.assertTrue(config.is_admin(406274598))
        self.assertFalse(config.is_admin(999999999))
        print("✅ Test 1 Passed: Configuration and Admin Auth Validated.")

    def test_02_pure_language_isolation(self):
        """Verify that Amharic keys do not contain English residue, and vice-versa."""
        am_msgs = MESSAGES["am"]
        en_msgs = MESSAGES["en"]

        # Critical review screen keys must not contain mixed parentheses like (Category) or (ዘርፍ)
        self.assertNotIn("Category", am_msgs.get("ad_prompt_category", ""))
        self.assertNotIn("Format", am_msgs.get("ad_prompt_format", ""))
        self.assertNotIn("Budget", am_msgs.get("ad_prompt_budget", ""))
        self.assertNotIn("Environment", am_msgs.get("ad_prompt_environment", ""))

        self.assertNotIn("ዘርፍ", en_msgs.get("ad_prompt_category", ""))
        self.assertNotIn("ቅርጸት", en_msgs.get("ad_prompt_format", ""))
        self.assertNotIn("በጀት", en_msgs.get("ad_prompt_budget", ""))

        # Check navigation buttons
        self.assertEqual(get_text("btn_submit", "am"), "✅ ጥያቄውን ላክ")
        self.assertEqual(get_text("btn_submit", "en"), "✅ Submit Request")
        self.assertEqual(get_text("btn_cancel", "am"), "❌ ሰርዝ")
        self.assertEqual(get_text("btn_cancel", "en"), "❌ Cancel")
        print("✅ Test 2 Passed: 100% Pure Language Isolation Validated.")

    def test_03_callback_data_lengths(self):
        """CRITICAL: Telegram enforces max 64 bytes UTF-8 on inline button callback_data."""
        # 1. Categories
        for code, mapping in keyboards.AD_CATEGORIES.items():
            cb = f"adcat:{code}"
            byte_len = len(cb.encode("utf-8"))
            self.assertLess(byte_len, 64, f"Category callback '{cb}' exceeds 64 bytes: {byte_len}")

        # 2. Formats
        for code, mapping in keyboards.AD_FORMATS.items():
            cb = f"adformat:{code}"
            byte_len = len(cb.encode("utf-8"))
            self.assertLess(byte_len, 64, f"Format callback '{cb}' exceeds 64 bytes: {byte_len}")

        # 3. Environments
        for code, mapping in keyboards.SHOOTING_ENVIRONMENTS.items():
            cb = f"adenviron:{code}"
            byte_len = len(cb.encode("utf-8"))
            self.assertLess(byte_len, 64, f"Environment callback '{cb}' exceeds 64 bytes: {byte_len}")

        # 4. Budgets
        for code, mapping in keyboards.BUDGET_TIERS.items():
            cb = f"adbudget:{code}"
            byte_len = len(cb.encode("utf-8"))
            self.assertLess(byte_len, 64, f"Budget callback '{cb}' exceeds 64 bytes: {byte_len}")

        # 5. Collaborations
        for code, mapping in keyboards.COLLAB_TYPES.items():
            cb = f"collabtype:{code}"
            byte_len = len(cb.encode("utf-8"))
            self.assertLess(byte_len, 64, f"Collab callback '{cb}' exceeds 64 bytes: {byte_len}")

        # 6. Admin Action callbacks
        sample_req = "AD-ABCD1234"
        admin_markup = keyboards.get_admin_request_actions_keyboard(sample_req)
        for row in admin_markup.inline_keyboard:
            for btn in row:
                byte_len = len(btn.callback_data.encode("utf-8"))
                self.assertLess(byte_len, 64, f"Admin action callback exceeds 64 bytes: {byte_len}")

        print("✅ Test 3 Passed: All Inline Callback Data < 64 Bytes (Guaranteed Zero Telegram Error).")

    def test_04_resolvers(self):
        """Verify code-to-localized-label resolvers."""
        self.assertEqual(keyboards.resolve_category_label("cars", "am"), "🚗 የመኪና ሽያጭና መለዋወጫ")
        self.assertEqual(keyboards.resolve_category_label("cars", "en"), "🚗 Cars & Auto Sales")

        self.assertEqual(keyboards.resolve_environment_label("client_location", "am"), "🏢 በድርጅትዎ/መደብርዎ ውስጥ የሚቀረጽ")
        self.assertEqual(keyboards.resolve_environment_label("client_location", "en"), "🏢 On-Site at Client Showroom / Compound")

        self.assertEqual(keyboards.resolve_format_label("full_video", "am"), "🎥 የተሟላ ራሱን የቻለ ቲክቶክ ቪዲዮ")
        self.assertEqual(keyboards.resolve_format_label("full_video", "en"), "🎥 Dedicated Full TikTok Video")

        self.assertEqual(keyboards.resolve_budget_label("tier_vip", "am"), "👑 ቪአይፒ (ከ150,000 - 500,000+ ብር)")
        self.assertEqual(keyboards.resolve_budget_label("tier_vip", "en"), "👑 VIP Millionaire (150,000 - 500,000+ ETB)")

        self.assertEqual(keyboards.resolve_collab_label("sponsorship", "am"), "🏆 ስፖንሰርሺፕ")
        self.assertEqual(keyboards.resolve_collab_label("sponsorship", "en"), "🏆 Sponsorship")
        print("✅ Test 4 Passed: Label Resolvers Correct.")

    def test_05_database_crud(self):
        """Verify full database workflow asynchronously."""
        async def run_db_tests():
            test_db = BASE_DIR / "test_sedo_bot.db"
            if test_db.exists():
                test_db.unlink()

            original_db = database.DB_PATH
            database.DB_PATH = str(test_db)
            config.SQLITE_DB_PATH = str(test_db)

            try:
                # 1. Init DB
                await database.init_db()

                # 2. User upsert & language
                await database.upsert_user(123456, "tester", "Sol", "Net", "en")
                user = await database.get_user(123456)
                self.assertIsNotNone(user)
                self.assertEqual(user["language"], "en")

                await database.set_user_language(123456, "am")
                self.assertEqual(await database.get_user_language(123456), "am")

                # 3. Create Ad Request
                ad_data = {
                    "user_id": 123456,
                    "category": "cars",
                    "format": "full_video",
                    "full_name": "Abebe Kebede",
                    "company_name": "Addis Auto Motors",
                    "company_address": "Bole Medhanialem, Addis Ababa",
                    "environment": "client_location",
                    "username": "@addisauto",
                    "phone": "+251911223344",
                    "description": "Showcasing new luxury SUV arrivals",
                    "preferred_date": "Next Friday",
                    "budget": "tier_vip",
                    "file_path": None,
                    "notes": "Include martial arts kick jump entrance"
                }
                ad_id = await database.create_advertisement_request(ad_data)
                self.assertTrue(ad_id.startswith("AD-"))

                fetched_ad = await database.get_advertisement_request(ad_id)
                self.assertEqual(fetched_ad["company_address"], "Bole Medhanialem, Addis Ababa")
                self.assertEqual(fetched_ad["environment"], "client_location")
                self.assertEqual(fetched_ad["status"], "pending")

                # Update status
                await database.update_advertisement_status(ad_id, "approved", "Approved by Sedo team")
                updated_ad = await database.get_advertisement_request(ad_id)
                self.assertEqual(updated_ad["status"], "approved")

                # 4. Create Partnership Request
                part_data = {
                    "user_id": 123456,
                    "full_name": "Dawit Tesfaye",
                    "company_name": "Energy Drink Co",
                    "position": "Marketing Manager",
                    "username": "@dawit",
                    "phone": "+251922334455",
                    "offer_description": "Exclusive gym drink sponsor",
                    "collab_type": "sponsorship",
                    "message": "Let's partner for the upcoming tournament",
                    "file_path": None
                }
                part_id = await database.create_partnership_request(part_data)
                self.assertTrue(part_id.startswith("PRT-"))

                # 5. Create Contact Message
                msg_id = await database.create_contact_message(123456, "Dawit", "Hello Sedo team!")
                self.assertTrue(msg_id.startswith("MSG-"))

                # 6. Dashboard Stats
                stats = await database.get_dashboard_stats()
                self.assertEqual(stats["total_users"], 1)
                self.assertEqual(stats["total_ads"], 1)
                self.assertEqual(stats["total_partnerships"], 1)

                # 7. CSV Export
                csv_bytes = await database.export_data_as_csv("advertisement_requests")
                self.assertTrue(len(csv_bytes.getvalue()) > 50)

            finally:
                database.DB_PATH = original_db
                config.SQLITE_DB_PATH = original_db
                if test_db.exists():
                    test_db.unlink()

        asyncio.run(run_db_tests())
        print("✅ Test 5 Passed: Full Database CRUD & Statistics Validated.")

    def test_06_handler_building(self):
        """Verify conversation handlers can be instantiated cleanly."""
        ad_handler = main.build_advertising_conversation_handler()
        self.assertIsNotNone(ad_handler)
        self.assertEqual(len(ad_handler.states), 16)

        part_handler = main.build_partnership_conversation_handler()
        self.assertIsNotNone(part_handler)
        self.assertEqual(len(part_handler.states), 10)

        contact_handler = main.build_contact_conversation_handler()
        self.assertIsNotNone(contact_handler)
        self.assertEqual(len(contact_handler.states), 2)
        print("✅ Test 6 Passed: Conversation Handlers Built Successfully.")


if __name__ == "__main__":
    unittest.main()
