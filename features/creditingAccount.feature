Feature: Crediting account
    As a service I want to credit an account

    Scenario: Crediting account
        Given an account 1234 has balance 0
        When an account 1234 is credited with 10
        Then a account 1234 should have a balance of 10
