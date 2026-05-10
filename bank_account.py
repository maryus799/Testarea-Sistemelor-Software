"""
BankAccount - clasa pentru gestionarea unui cont bancar simplu.
Folosita ca subiect de testare unitara in cadrul T1.
"""


class BankAccount:
    """
    Reprezinta un cont bancar cu operatii de baza:
    depunere, retragere si transfer intre conturi.

    Atribute:
        owner (str): Numele titularului contului
        balance (float): Soldul curent al contului
        is_active (bool): Starea contului (activ/inactiv)
    """

    MAX_DEPOSIT = 10000.0
    MAX_WITHDRAWAL = 5000.0
    MIN_BALANCE = 0.0

    def __init__(self, owner: str, initial_balance: float = 0.0):
        """
        Initializeaza un cont bancar.

        Args:
            owner: Numele titularului (nu poate fi gol)
            initial_balance: Soldul initial (implicit 0, nu poate fi negativ)

        Raises:
            ValueError: daca owner este gol sau initial_balance este negativ
        """
        if not owner or not owner.strip():
            raise ValueError("Numele titularului nu poate fi gol.")
        if initial_balance < 0:
            raise ValueError("Soldul initial nu poate fi negativ.")

        self.owner = owner.strip()
        self.balance = initial_balance
        self.is_active = True

    def deposit(self, amount: float) -> float:
        """
        Depune o suma in cont.

        Args:
            amount: Suma de depus (trebuie sa fie > 0 si <= MAX_DEPOSIT)

        Returns:
            Noul sold al contului

        Raises:
            ValueError: daca contul este inactiv, suma <= 0 sau suma > MAX_DEPOSIT
        """
        if not self.is_active:
            raise ValueError("Contul este inactiv.")
        if amount <= 0:
            raise ValueError("Suma de depus trebuie sa fie pozitiva.")
        if amount > self.MAX_DEPOSIT:
            raise ValueError(f"Suma depaseste limita maxima de depunere ({self.MAX_DEPOSIT}).")

        self.balance += amount
        return self.balance

    def withdraw(self, amount: float) -> float:
        """
        Retrage o suma din cont.

        Args:
            amount: Suma de retras (trebuie sa fie > 0, <= MAX_WITHDRAWAL si <= balance)

        Returns:
            Noul sold al contului

        Raises:
            ValueError: daca contul este inactiv, suma invalida sau fonduri insuficiente
        """
        if not self.is_active:
            raise ValueError("Contul este inactiv.")
        if amount <= 0:
            raise ValueError("Suma de retras trebuie sa fie pozitiva.")
        if amount > self.MAX_WITHDRAWAL:
            raise ValueError(f"Suma depaseste limita maxima de retragere ({self.MAX_WITHDRAWAL}).")
        if amount > self.balance:
            raise ValueError("Fonduri insuficiente.")

        self.balance -= amount
        return self.balance

    def transfer(self, target: "BankAccount", amount: float) -> float:
        """
        Transfera o suma catre un alt cont.

        Args:
            target: Contul destinatar
            amount: Suma de transferat

        Returns:
            Noul sold al contului sursa

        Raises:
            ValueError: daca target este None, conturile sunt identice sau transfer esueaza
        """
        if target is None or not isinstance(target, BankAccount):
            raise ValueError("Contul destinatar trebuie sa fie un BankAccount valid.")
        if target is self:
            raise ValueError("Nu se poate transfera catre acelasi cont.")
        if not target.is_active:
            raise ValueError("Contul destinatar este inactiv.")

        self.withdraw(amount)
        target.deposit(amount)
        return self.balance

    def deposit_multiple(self, amounts: list, min_amount: float = 0.0, max_amount: float = None) -> float:
        """
        Depune mai multe sume succesiv in cont.

        Contine:
        - instructiune repetitiva (for)
        - if fara else (validari initiale)
        - if cu else (verificare interval suma)
        - conditie simpla: if not self.is_active
        - conditie compusa: if amount is not None and amount >= min_amount

        Args:
            amounts: Lista de sume de depus
            min_amount: Suma minima acceptata (implicit 0.0)
            max_amount: Suma maxima acceptata (implicit None = fara limita superioara)

        Returns:
            Noul sold dupa toate depunerile valide

        Raises:
            ValueError: daca lista este goala, contul este inactiv sau nicio suma valida
        """
        if not self.is_active:
            raise ValueError("Contul este inactiv.")
        if not amounts:
            raise ValueError("Lista de sume nu poate fi goala.")
        if min_amount < 0:
            raise ValueError("Suma minima nu poate fi negativa.")

        depuneri_valide = 0
        for amount in amounts:
            if amount is not None and amount > min_amount:
                if max_amount is not None and amount > max_amount:
                    pass  # suma depaseste maximul, se sare
                else:
                    self.deposit(amount)
                    depuneri_valide += 1

        if depuneri_valide == 0:
            raise ValueError("Nicio suma valida in lista.")

        return self.balance

    def close(self) -> None:
        """Inchide contul (il marcheaza ca inactiv)."""
        self.is_active = False

    def get_balance(self) -> float:
        """Returneaza soldul curent."""
        return self.balance

    def __str__(self) -> str:
        status = "activ" if self.is_active else "inactiv"
        return f"BankAccount(owner='{self.owner}', balance={self.balance:.2f}, status={status})"
