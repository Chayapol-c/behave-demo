Feature: Github User
    Scenario Outline: An authenticated user can get email address of a Github acct.
        This is a test of the Github /users/{username} API endpoint.
        Given I am an authenticated user
        When  I query the user data for "<username>"
        Then  the email is <email>
        And   the name is "<name>"
        Examples:
            | username   | email                  | name                     |
            | Chayapol-c | chayapol.cha@gmail.com | Chayapol Chaipongsawalee |
            | fatalaijon | fatalaijon@gmail.com   | Jon Fatalai              |
            | parujr     | null                   | Paruj Ratanaworabhan     |