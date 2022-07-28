Feature: fakebros scrapping

Scenario: The one where I find all events related to a tweet
    Given I have logged in twitter
    And I know how much tweets, likes and shares related to the search "Liverpool.  Com isso City abre 10 pontos de vantagem no topo da #PL  C'MOOOOON CITY!!!!" there is
    When I scrap the tweet
    Then I should get all likers and sharers of the tweet

