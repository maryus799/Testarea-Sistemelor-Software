"""
Teste generate automat de Claude (AI) pentru clasa BankAccount.
Folosite pentru comparatie cu testele scrise manual.
Prompt dat: "Generate pytest unit tests for a Python BankAccount class
with methods deposit(amount), withdraw(amount), transfer(target, amount),
deposit_multiple(amounts, min_amount, max_amount)"
Data generarii: 25 mai 2026
"""

import pytest
from bank_account import BankAccount


class TestBankAccountAI:

    def setup_method(self):
        self.account = BankAccount("Test User", 1000.0)

    # --- deposit ---
    def test_deposit_positive_amount(self):
        self.account.deposit(500)
        assert self.account.balance == 1500

    def test_deposit_zero_raises(self):
        with pytest.raises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_raises(self):
        with pytest.raises(ValueError):
            self.account.deposit(-100)

    def test_deposit_exceeds_max_raises(self):
        with pytest.raises(ValueError):
            self.account.deposit(10001)

    def test_deposit_inactive_raises(self):
        self.account.close()
        with pytest.raises(ValueError):
            self.account.deposit(100)

    # --- withdraw ---
    def test_withdraw_valid(self):
        self.account.withdraw(500)
        assert self.account.balance == 500

    def test_withdraw_zero_raises(self):
        with pytest.raises(ValueError):
            self.account.withdraw(0)

    def test_withdraw_negative_raises(self):
        with pytest.raises(ValueError):
            self.account.withdraw(-50)

    def test_withdraw_exceeds_max_raises(self):
        with pytest.raises(ValueError):
            self.account.withdraw(5001)

    def test_withdraw_insufficient_funds_raises(self):
        with pytest.raises(ValueError):
            self.account.withdraw(2000)

    def test_withdraw_inactive_raises(self):
        self.account.close()
        with pytest.raises(ValueError):
            self.account.withdraw(100)

    # --- transfer ---
    def test_transfer_valid(self):
        target = BankAccount("Target", 0)
        self.account.transfer(target, 300)
        assert self.account.balance == 700
        assert target.balance == 300

    def test_transfer_none_target_raises(self):
        with pytest.raises(ValueError):
            self.account.transfer(None, 100)

    def test_transfer_same_account_raises(self):
        with pytest.raises(ValueError):
            self.account.transfer(self.account, 100)

    def test_transfer_inactive_target_raises(self):
        target = BankAccount("Target", 0)
        target.close()
        with pytest.raises(ValueError):
            self.account.transfer(target, 100)

    # --- deposit_multiple ---
    def test_deposit_multiple_valid(self):
        self.account.deposit_multiple([100, 200, 300])
        assert self.account.balance == 1600

    def test_deposit_multiple_empty_raises(self):
        with pytest.raises(ValueError):
            self.account.deposit_multiple([])

    def test_deposit_multiple_all_invalid_raises(self):
        with pytest.raises(ValueError):
            self.account.deposit_multiple([-100, None])

    def test_deposit_multiple_with_max(self):
        self.account.deposit_multiple([100, 500], max_amount=200)
        assert self.account.balance == 1100

    def test_deposit_multiple_with_min(self):
        self.account.deposit_multiple([50, 100, 200], min_amount=100)
        assert self.account.balance == 1200
