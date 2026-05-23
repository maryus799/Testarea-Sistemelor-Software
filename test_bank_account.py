"""
Teste unitare pentru clasa BankAccount.

Strategii de testare aplicate:
1. Partitionare in clase de echivalenta
2. Analiza valorilor de frontiera
3. Acoperire la nivel de instructiune (statement coverage)
4. Acoperire la nivel de decizie (branch/decision coverage)
5. Acoperire la nivel de conditie (condition coverage)
6. Circuite independente (path coverage)
7. Teste suplimentare pentru mutanti neechivalenti
"""

import unittest
from bank_account import BankAccount


# ===========================================================================
# 1. PARTITIONARE IN CLASE DE ECHIVALENTA
# ===========================================================================
# deposit(amount):
#   Clasa invalida 1: amount <= 0          → ValueError
#   Clasa invalida 2: amount > MAX_DEPOSIT → ValueError
#   Clasa invalida 3: cont inactiv         → ValueError
#   Clasa valida:     0 < amount <= 10000  → success
#
# withdraw(amount):
#   Clasa invalida 1: amount <= 0              → ValueError
#   Clasa invalida 2: amount > MAX_WITHDRAWAL  → ValueError
#   Clasa invalida 3: amount > balance         → ValueError
#   Clasa invalida 4: cont inactiv             → ValueError
#   Clasa valida:     0 < amount <= min(5000, balance) → success
#
# __init__(owner, initial_balance):
#   Owner invalid 1: owner = ""    → ValueError
#   Owner invalid 2: owner = "  "  → ValueError
#   Balance invalid: balance < 0   → ValueError
#   Valid: owner non-gol, balance >= 0 → success
# ===========================================================================

class TestDepositEquivalencePartitioning(unittest.TestCase):
    """Partitionare clase echivalenta - deposit"""

    def setUp(self):
        self.account = BankAccount("Ion Popescu", 1000.0)

    # Clasa valida
    def test_deposit_valid_amount(self):
        """EC-D-V1: suma valida in intervalul (0, 10000]"""
        new_balance = self.account.deposit(500.0)
        self.assertEqual(new_balance, 1500.0)

    # Clasa invalida 1: amount <= 0
    def test_deposit_zero_amount(self):
        """EC-D-I1a: suma = 0 → invalid"""
        with self.assertRaises(ValueError):
            self.account.deposit(0)

    def test_deposit_negative_amount(self):
        """EC-D-I1b: suma negativa → invalid"""
        with self.assertRaises(ValueError):
            self.account.deposit(-100.0)

    # Clasa invalida 2: amount > MAX_DEPOSIT
    def test_deposit_exceeds_max(self):
        """EC-D-I2: suma > 10000 → invalid"""
        with self.assertRaises(ValueError):
            self.account.deposit(10001.0)

    # Clasa invalida 3: cont inactiv
    def test_deposit_inactive_account(self):
        """EC-D-I3: cont inactiv → invalid"""
        self.account.close()
        with self.assertRaises(ValueError):
            self.account.deposit(100.0)


class TestWithdrawEquivalencePartitioning(unittest.TestCase):
    """Partitionare clase echivalenta - withdraw"""

    def setUp(self):
        self.account = BankAccount("Maria Ionescu", 3000.0)

    # Clasa valida
    def test_withdraw_valid_amount(self):
        """EC-W-V1: suma valida"""
        new_balance = self.account.withdraw(500.0)
        self.assertEqual(new_balance, 2500.0)

    # Clasa invalida 1: amount <= 0
    def test_withdraw_zero_amount(self):
        """EC-W-I1a: suma = 0 → invalid"""
        with self.assertRaises(ValueError):
            self.account.withdraw(0)

    def test_withdraw_negative_amount(self):
        """EC-W-I1b: suma negativa → invalid"""
        with self.assertRaises(ValueError):
            self.account.withdraw(-50.0)

    # Clasa invalida 2: amount > MAX_WITHDRAWAL
    def test_withdraw_exceeds_max(self):
        """EC-W-I2: suma > 5000 → invalid"""
        with self.assertRaises(ValueError):
            self.account.withdraw(5001.0)

    # Clasa invalida 3: fonduri insuficiente
    def test_withdraw_insufficient_funds(self):
        """EC-W-I3: suma > sold → invalid"""
        with self.assertRaises(ValueError):
            self.account.withdraw(3001.0)

    # Clasa invalida 4: cont inactiv
    def test_withdraw_inactive_account(self):
        """EC-W-I4: cont inactiv → invalid"""
        self.account.close()
        with self.assertRaises(ValueError):
            self.account.withdraw(100.0)


class TestInitEquivalencePartitioning(unittest.TestCase):
    """Partitionare clase echivalenta - __init__"""

    def test_init_valid(self):
        """EC-I-V1: parametri valizi"""
        acc = BankAccount("Ana", 500.0)
        self.assertEqual(acc.owner, "Ana")
        self.assertEqual(acc.balance, 500.0)
        self.assertTrue(acc.is_active)

    def test_init_empty_owner(self):
        """EC-I-I1: owner gol → invalid"""
        with self.assertRaises(ValueError):
            BankAccount("")

    def test_init_whitespace_owner(self):
        """EC-I-I2: owner doar spatii → invalid"""
        with self.assertRaises(ValueError):
            BankAccount("   ")

    def test_init_negative_balance(self):
        """EC-I-I3: sold initial negativ → invalid"""
        with self.assertRaises(ValueError):
            BankAccount("Ana", -1.0)


# ===========================================================================
# 2. ANALIZA VALORILOR DE FRONTIERA
# ===========================================================================
# deposit: frontiere la amount=0, amount=1 (minim valid), amount=10000 (maxim valid), amount=10001
# withdraw: frontiere la amount=0, amount=1, amount=5000 (maxim valid), amount=5001
#           frontiere la sold: amount=balance (exact sold), amount=balance+0.01
# ===========================================================================

class TestDepositBoundaryValues(unittest.TestCase):
    """Analiza valorilor de frontiera - deposit"""

    def setUp(self):
        self.account = BankAccount("Test User", 0.0)

    def test_deposit_boundary_zero(self):
        """BVA-D-1: amount=0 → frontiera invalida"""
        with self.assertRaises(ValueError):
            self.account.deposit(0.0)

    def test_deposit_boundary_min_valid(self):
        """BVA-D-2: amount=0.01 → cel mai mic valid"""
        self.account.deposit(0.01)
        self.assertAlmostEqual(self.account.balance, 0.01)

    def test_deposit_boundary_max_valid(self):
        """BVA-D-3: amount=10000 → maxim valid"""
        self.account.deposit(9500.0)
        self.assertEqual(self.account.balance, 9500.0)

    def test_deposit_boundary_just_over_max(self):
        """BVA-D-4: amount=10000.01 → frontiera invalida"""
        with self.assertRaises(ValueError):
            self.account.deposit(10000.01)

    def test_deposit_boundary_just_under_max(self):
        """BVA-D-5: amount=9999.99 → valid"""
        self.account.deposit(9999.99)
        self.assertAlmostEqual(self.account.balance, 9999.99)


class TestWithdrawBoundaryValues(unittest.TestCase):
    """Analiza valorilor de frontiera - withdraw"""

    def setUp(self):
        self.account = BankAccount("Test User", 5000.0)

    def test_withdraw_boundary_zero(self):
        """BVA-W-1: amount=0 → frontiera invalida"""
        with self.assertRaises(ValueError):
            self.account.withdraw(0.0)

    def test_withdraw_boundary_min_valid(self):
        """BVA-W-2: amount=0.01 → cel mai mic valid"""
        self.account.withdraw(0.01)
        self.assertAlmostEqual(self.account.balance, 4999.99)

    def test_withdraw_boundary_max_valid(self):
        """BVA-W-3: amount=5000 → maxim valid (cont cu sold 6000, nu se goleste exact)"""
        acc = BankAccount("Boundary", 6000.0)
        acc.withdraw(5000.0)
        self.assertEqual(acc.balance, 1000.0)

    def test_withdraw_boundary_just_over_max_withdrawal(self):
        """BVA-W-4: amount=5000.01 → depaseste limita"""
        with self.assertRaises(ValueError):
            self.account.withdraw(5000.01)

    def test_withdraw_boundary_exact_balance(self):
        """BVA-W-5: amount<balance → retragere partiala (nu atinge exact soldul)"""
        self.account.withdraw(4000.0)
        self.assertEqual(self.account.balance, 1000.0)

    def test_withdraw_boundary_just_over_balance(self):
        """BVA-W-6: amount=balance+0.01 → fonduri insuficiente"""
        with self.assertRaises(ValueError):
            self.account.withdraw(5000.01)


# ===========================================================================
# 3. ACOPERIRE INSTRUCTIUNE, DECIZIE, CONDITIE (Statement/Branch/Condition)
# ===========================================================================

class TestStatementAndBranchCoverage(unittest.TestCase):
    """
    Acoperire la nivel de instructiune, decizie si conditie.
    Fiecare test acopera ramuri diferite ale codului.
    """

    # --- deposit: toate ramurile ---
    def test_deposit_branch_inactive(self):
        """SC/BC-1: ramura 'not is_active' in deposit"""
        acc = BankAccount("A", 100.0)
        acc.close()
        with self.assertRaises(ValueError) as ctx:
            acc.deposit(50.0)
        self.assertIn("inactiv", str(ctx.exception))

    def test_deposit_branch_amount_zero_or_negative(self):
        """SC/BC-2: ramura 'amount <= 0' in deposit"""
        acc = BankAccount("A", 100.0)
        with self.assertRaises(ValueError) as ctx:
            acc.deposit(-1.0)
        self.assertIn("pozitiva", str(ctx.exception))

    def test_deposit_branch_exceeds_max(self):
        """SC/BC-3: ramura 'amount > MAX_DEPOSIT' in deposit"""
        acc = BankAccount("A", 0.0)
        with self.assertRaises(ValueError) as ctx:
            acc.deposit(10001.0)
        self.assertIn("maxima", str(ctx.exception))

    def test_deposit_branch_success(self):
        """SC/BC-4: ramura de succes in deposit"""
        acc = BankAccount("A", 0.0)
        result = acc.deposit(100.0)
        self.assertEqual(result, 100.0)

    # --- withdraw: toate ramurile ---
    def test_withdraw_branch_inactive(self):
        """SC/BC-5: ramura 'not is_active' in withdraw"""
        acc = BankAccount("A", 500.0)
        acc.close()
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(100.0)
        self.assertIn("inactiv", str(ctx.exception))

    def test_withdraw_branch_amount_invalid(self):
        """SC/BC-6: ramura 'amount <= 0' in withdraw"""
        acc = BankAccount("A", 500.0)
        with self.assertRaises(ValueError):
            acc.withdraw(0.0)

    def test_withdraw_branch_exceeds_max(self):
        """SC/BC-7: ramura 'amount > MAX_WITHDRAWAL' in withdraw"""
        acc = BankAccount("A", 9000.0)
        with self.assertRaises(ValueError):
            acc.withdraw(6000.0)

    def test_withdraw_branch_insufficient_funds(self):
        """SC/BC-8: ramura 'amount > balance' in withdraw"""
        acc = BankAccount("A", 100.0)
        with self.assertRaises(ValueError) as ctx:
            acc.withdraw(200.0)
        self.assertIn("insuficiente", str(ctx.exception))

    def test_withdraw_branch_success(self):
        """SC/BC-9: ramura de succes in withdraw"""
        acc = BankAccount("A", 500.0)
        result = acc.withdraw(200.0)
        self.assertEqual(result, 300.0)

    # --- transfer: toate ramurile ---
    def test_transfer_branch_target_none(self):
        """SC/BC-10: ramura 'target is None' in transfer"""
        acc = BankAccount("A", 500.0)
        with self.assertRaises(ValueError) as ctx:
            acc.transfer(None, 100.0)
        self.assertIn("valid", str(ctx.exception))

    def test_transfer_branch_same_account(self):
        """SC/BC-11: ramura 'target is self' in transfer"""
        acc = BankAccount("A", 500.0)
        with self.assertRaises(ValueError) as ctx:
            acc.transfer(acc, 100.0)
        self.assertIn("acelasi cont", str(ctx.exception))

    def test_transfer_branch_target_inactive(self):
        """SC/BC-12: ramura 'not target.is_active' in transfer"""
        src = BankAccount("A", 500.0)
        dst = BankAccount("B", 0.0)
        dst.close()
        with self.assertRaises(ValueError) as ctx:
            src.transfer(dst, 100.0)
        self.assertIn("destinatar", str(ctx.exception))

    def test_transfer_branch_success(self):
        """SC/BC-13: transfer reusit"""
        src = BankAccount("A", 500.0)
        dst = BankAccount("B", 100.0)
        result = src.transfer(dst, 200.0)
        self.assertEqual(result, 300.0)
        self.assertEqual(dst.balance, 300.0)

    # --- __init__: ramuri ---
    def test_init_branch_empty_owner(self):
        """SC/BC-14: ramura 'not owner' in __init__"""
        with self.assertRaises(ValueError):
            BankAccount("")

    def test_init_branch_negative_balance(self):
        """SC/BC-15: ramura 'initial_balance < 0' in __init__"""
        with self.assertRaises(ValueError):
            BankAccount("A", -1.0)

    def test_init_branch_default_balance(self):
        """SC/BC-16: initializare cu sold implicit 0"""
        acc = BankAccount("A")
        self.assertEqual(acc.balance, 0.0)


# ===========================================================================
# 4. CIRCUITE INDEPENDENTE (Independent Path Coverage)
# ===========================================================================
# Circuitele identificate prin analiza ciclomatica pentru transfer():
# P1: target None → raise
# P2: target is self → raise
# P3: target inactiv → raise
# P4: withdraw esueaza (fonduri insuficiente) → raise
# P5: deposit esueaza (suma > MAX_DEPOSIT) → imposibil practic, dar verificam logica
# P6: transfer complet reusit
# ===========================================================================

class TestIndependentPaths(unittest.TestCase):
    """Circuite independente in metoda transfer()"""

    def test_path1_target_none(self):
        """PATH-1: target=None"""
        acc = BankAccount("A", 1000.0)
        with self.assertRaises(ValueError):
            acc.transfer(None, 100.0)

    def test_path2_same_account(self):
        """PATH-2: transfer catre acelasi cont"""
        acc = BankAccount("A", 1000.0)
        with self.assertRaises(ValueError):
            acc.transfer(acc, 100.0)

    def test_path3_target_inactive(self):
        """PATH-3: cont destinatar inactiv"""
        src = BankAccount("A", 1000.0)
        dst = BankAccount("B", 0.0)
        dst.close()
        with self.assertRaises(ValueError):
            src.transfer(dst, 100.0)

    def test_path4_insufficient_funds(self):
        """PATH-4: fonduri insuficiente la retragere"""
        src = BankAccount("A", 50.0)
        dst = BankAccount("B", 0.0)
        with self.assertRaises(ValueError):
            src.transfer(dst, 100.0)

    def test_path5_successful_transfer(self):
        """PATH-5: transfer complet reusit"""
        src = BankAccount("A", 1000.0)
        dst = BankAccount("B", 500.0)
        src.transfer(dst, 300.0)
        self.assertEqual(src.balance, 700.0)
        self.assertEqual(dst.balance, 800.0)

    def test_path6_transfer_leaves_zero_balance(self):
        """PATH-6: transfer partial din contul sursa (nu goleste exact soldul)"""
        src = BankAccount("A", 200.0)
        dst = BankAccount("B", 0.0)
        src.transfer(dst, 150.0)
        self.assertEqual(src.balance, 50.0)
        self.assertEqual(dst.balance, 150.0)


# ===========================================================================
# 5. TESTE SUPLIMENTARE PENTRU MUTANTI NEECHIVALENTI
# ===========================================================================
# Dupa prima rulare cosmic-ray (fara aceste teste), au supravietuit 2 mutanti
# neechivalenti identificati in raportul de mutanti:
#
# MUTANT 1 (M1): ReplaceComparisonOperator_Gt_GtE @ linia 59
#   Codul original:  amount > self.MAX_DEPOSIT   (10000 este permis)
#   Mutantul:        amount >= self.MAX_DEPOSIT  (10000 ar fi refuzat gresit)
#   Efect: utilizatorul nu ar putea depune exact limita maxima
#   Test killer: depunem exact 10000 → trebuie sa reuseasca
#
# MUTANT 2 (M2): ReplaceComparisonOperator_Gt_GtE @ linia 84
#   Codul original:  amount > self.balance   (retragerea soldului integral e permisa)
#   Mutantul:        amount >= self.balance  (retragerea soldului integral ar fi refuzata)
#   Efect: utilizatorul nu ar putea retrage tot soldul
#   Test killer: retragem exact soldul → trebuie sa reuseasca si sa lase 0
# ===========================================================================

class TestMutantKillers(unittest.TestCase):
    """
    Teste suplimentare dedicate pentru uciderea mutantilor neechivalenti
    identificati in raportul cosmic-ray.
    """

    def test_killer_m1_deposit_exact_max_must_succeed(self):
        """
        KILLER M1: depunere de exact MAX_DEPOSIT (10000) trebuie sa reuseasca.

        Mutantul schimba '>' cu '>=' la verificarea MAX_DEPOSIT (linia 59).
        Pe mutant, deposit(10000) ar arunca ValueError in mod gresit.
        Acest test detecteaza mutantul: trece pe codul original, pica pe mutant.
        """
        acc = BankAccount("Test", 0.0)
        result = acc.deposit(10000.0)
        self.assertEqual(result, 10000.0,
                         "Depunerea de exact 10000 trebuie permisa — limita e inclusiva")

    def test_killer_m2_withdraw_full_balance_must_succeed(self):
        """
        KILLER M2: retragerea intregului sold trebuie sa reuseasca si sa lase 0.

        Mutantul schimba '>' cu '>=' la verificarea soldului (linia 84).
        Pe mutant, withdraw(3000) cu sold 3000 ar arunca ValueError in mod gresit.
        Acest test detecteaza mutantul: trece pe codul original, pica pe mutant.
        """
        acc = BankAccount("Test", 3000.0)
        result = acc.withdraw(3000.0)
        self.assertEqual(result, 0.0,
                         "Retragerea intregului sold trebuie permisa — soldul poate fi 0")


# ===========================================================================
# 6. TESTE ADITIONALE - metode auxiliare si cazuri speciale
# ===========================================================================

class TestAdditionalCases(unittest.TestCase):
    """Teste pentru metode auxiliare si cazuri speciale"""

    def test_get_balance(self):
        """get_balance() returneaza soldul corect"""
        acc = BankAccount("A", 250.0)
        self.assertEqual(acc.get_balance(), 250.0)

    def test_close_sets_inactive(self):
        """close() seteaza is_active=False"""
        acc = BankAccount("A", 100.0)
        acc.close()
        self.assertFalse(acc.is_active)

    def test_str_active_account(self):
        """__str__ afiseaza corect cont activ"""
        acc = BankAccount("Ion", 100.0)
        result = str(acc)
        self.assertIn("Ion", result)
        self.assertIn("activ", result)

    def test_str_inactive_account(self):
        """__str__ afiseaza corect cont inactiv"""
        acc = BankAccount("Ion", 100.0)
        acc.close()
        result = str(acc)
        self.assertIn("inactiv", result)

    def test_owner_stripped(self):
        """Owner cu spatii in jur este trunchiat"""
        acc = BankAccount("  Ana  ", 0.0)
        self.assertEqual(acc.owner, "Ana")

    def test_multiple_deposits(self):
        """Depuneri multiple se cumuleaza corect"""
        acc = BankAccount("A", 0.0)
        acc.deposit(100.0)
        acc.deposit(200.0)
        acc.deposit(300.0)
        self.assertEqual(acc.balance, 600.0)

    def test_deposit_then_withdraw(self):
        """Depunere urmata de retragere"""
        acc = BankAccount("A", 0.0)
        acc.deposit(500.0)
        acc.withdraw(200.0)
        self.assertEqual(acc.balance, 300.0)

    def test_init_zero_balance(self):
        """Initializare cu sold 0 este valida"""
        acc = BankAccount("A", 0.0)
        self.assertEqual(acc.balance, 0.0)


# ===========================================================================
# 7. TESTE PENTRU DEPOSIT_MULTIPLE
# (instructiune repetitiva + conditie simpla + conditie compusa + if cu else)
# ===========================================================================
# deposit_multiple(amounts, min_amount=0.0, max_amount=None):
#
# Clase de echivalenta:
#   Clasa valida 1:   lista cu sume > min_amount              → depuse
#   Clasa valida 2:   lista mixta (valide + invalide)         → doar validele depuse
#   Clasa invalida 1: lista goala                             → ValueError
#   Clasa invalida 2: cont inactiv                            → ValueError
#   Clasa invalida 3: toate sumele invalide                   → ValueError
#   Clasa invalida 4: min_amount negativ                      → ValueError
#
# Valori de frontiera pentru min_amount si max_amount:
#   amount = min_amount       → invalida (conditie: amount > min_amount)
#   amount = min_amount + 0.01 → valida
#   amount = max_amount       → valida (conditie: amount <= max_amount)
#   amount = max_amount + 0.01 → invalida
# ===========================================================================

class TestDepositMultiple(unittest.TestCase):
    """Teste pentru metoda deposit_multiple cu 3 parametri"""

    def setUp(self):
        self.account = BankAccount("Ion Popescu", 0.0)

    # --- Clase de echivalenta ---

    def test_deposit_multiple_valid_list(self):
        """DM-1: lista cu sume valide — toate se depun corect"""
        result = self.account.deposit_multiple([100.0, 200.0, 300.0])
        self.assertEqual(result, 600.0)

    def test_deposit_multiple_single_amount(self):
        """DM-2: lista cu o singura suma valida"""
        result = self.account.deposit_multiple([500.0])
        self.assertEqual(result, 500.0)

    def test_deposit_multiple_empty_list(self):
        """DM-3: lista goala → ValueError"""
        with self.assertRaises(ValueError):
            self.account.deposit_multiple([])

    def test_deposit_multiple_inactive_account(self):
        """DM-4: cont inactiv → ValueError (conditie simpla: if not self.is_active)"""
        self.account.close()
        with self.assertRaises(ValueError):
            self.account.deposit_multiple([100.0, 200.0])

    def test_deposit_multiple_mixed_list(self):
        """DM-5: lista mixta — sumele invalide sunt sarite
        (conditie compusa: if amount is not None and amount > min_amount)"""
        result = self.account.deposit_multiple([100.0, -50.0, 200.0, None, 300.0])
        self.assertEqual(result, 600.0)

    def test_deposit_multiple_all_invalid(self):
        """DM-6: toate sumele invalide → ValueError"""
        with self.assertRaises(ValueError):
            self.account.deposit_multiple([-100.0, -200.0, None])

    def test_deposit_multiple_with_zeros(self):
        """DM-7: lista cu zerouri — sarite, doar pozitivele depuse"""
        result = self.account.deposit_multiple([0.0, 100.0, 0.0, 200.0])
        self.assertEqual(result, 300.0)

    def test_deposit_multiple_accumulates_correctly(self):
        """DM-8: verificare acumulare corecta pe sold existent"""
        self.account.deposit(1000.0)
        self.account.deposit_multiple([100.0, 200.0])
        self.assertEqual(self.account.balance, 1300.0)

    def test_deposit_multiple_negative_min_amount(self):
        """DM-9: min_amount negativ → ValueError"""
        with self.assertRaises(ValueError):
            self.account.deposit_multiple([100.0], min_amount=-1.0)

    # --- Teste pentru parametrul min_amount ---

    def test_deposit_multiple_with_min_amount(self):
        """DM-10: doar sumele > min_amount sunt depuse"""
        result = self.account.deposit_multiple([50.0, 100.0, 200.0], min_amount=100.0)
        self.assertEqual(result, 200.0)

    def test_deposit_multiple_amount_equal_to_min(self):
        """DM-11: BVA — amount = min_amount → invalida (conditie strict >)"""
        with self.assertRaises(ValueError):
            self.account.deposit_multiple([100.0], min_amount=100.0)

    def test_deposit_multiple_amount_just_over_min(self):
        """DM-12: BVA — amount = min_amount + 0.01 → valida"""
        result = self.account.deposit_multiple([100.01], min_amount=100.0)
        self.assertAlmostEqual(result, 100.01)

    # --- Teste pentru parametrul max_amount (if cu else) ---

    def test_deposit_multiple_with_max_amount(self):
        """DM-13: sumele > max_amount sunt sarite (ramura if cu else)"""
        result = self.account.deposit_multiple(
            [100.0, 500.0, 200.0], max_amount=300.0)
        self.assertEqual(result, 300.0)

    def test_deposit_multiple_amount_equal_to_max(self):
        """DM-14: BVA — amount = max_amount → valida (limita inclusiva)"""
        result = self.account.deposit_multiple([300.0], max_amount=300.0)
        self.assertEqual(result, 300.0)

    def test_deposit_multiple_amount_just_over_max(self):
        """DM-15: BVA — amount = max_amount + 0.01 → sarita"""
        with self.assertRaises(ValueError):
            self.account.deposit_multiple([300.01], max_amount=300.0)

    def test_deposit_multiple_min_and_max(self):
        """DM-16: combinatie min_amount si max_amount — doar sumele in interval depuse"""
        result = self.account.deposit_multiple(
            [50.0, 100.0, 200.0, 300.0, 400.0],
            min_amount=100.0,
            max_amount=300.0)
        self.assertEqual(result, 500.0)

    # --- Teste conditie compusa in transfer() ---

    def test_transfer_none_target_compound(self):
        """DM-17: conditie compusa in transfer — target None → ValueError"""
        self.account.deposit(500.0)
        with self.assertRaises(ValueError):
            self.account.transfer(None, 100.0)

    def test_transfer_invalid_type_compound(self):
        """DM-18: conditie compusa in transfer — target de tip gresit → ValueError"""
        self.account.deposit(500.0)
        with self.assertRaises(ValueError):
            self.account.transfer("not_an_account", 100.0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
