-- Keep a log of any SQL queries you execute as you solve the mystery.

-- New info from this query:
-- 3 witnesses, each mentioned the word 'bakery'
-- theft of CS50 duck took place at 10:15am
SELECT description
FROM crime_scene_reports
WHERE year=2023 AND month=7 AND day=28 AND street='Humphrey Street';

-- New info from this query:
-- Thief drove away within 10mins, so before 10:25am, should check security footage
-- Thief withdrew money from ATM on Leggett St earlier that morning
-- Thief called someone and talked less than 1 min, thief said planning to take earliest
--   flight out of Fiftyville tomorrow. Thief asked the other person to purchase the
--   flight ticket
SELECT id, name, transcript
FROM interviews
WHERE year=2023 AND month=7 AND day=28 AND transcript LIKE '%bakery%';

-- Find the list of people who:
-- • were seen leaving the bakery between 10:15 AND 10:25
-- • making a phone call for less than a minute on that day
-- • withdrawing money at ATM on Leggett Street that morning
-- • leaving Fiftyville by plane the next morning (29 Jul 2023)
-- Answer: Bruce (id 686048), making a call to (375) 555-8161, would fly to airport id 4
SELECT p.id, p.name, p.phone_number, p.passport_number, pc.caller, pc.receiver, f.destination_airport_id
FROM atm_transactions at
INNER JOIN bank_accounts ba ON at.account_number = ba.account_number
INNER JOIN people p ON ba.person_id = p.id
INNER JOIN bakery_security_logs bsl ON p.license_plate = bsl.license_plate
INNER JOIN phone_calls pc ON pc.caller = p.phone_number
INNER JOIN passengers pp ON p.passport_number = pp.passport_number
INNER JOIN flights f ON pp.flight_id = f.id
INNER JOIN airports a ON f.origin_airport_id = a.id
WHERE at.year=2023 AND at.month=7 AND at.day=28
  AND at.atm_location='Leggett Street'
  AND at.transaction_type='withdraw'
  AND bsl.year=2023 AND bsl.month=7 AND bsl.day=28
  AND bsl.activity='exit' AND bsl.hour=10 AND bsl.minute BETWEEN 15 AND 25
  AND pc.year=2023 AND pc.month=7 AND pc.day=28 AND pc.duration <= 60
  AND a.city='Fiftyville'
  AND f.year=2023 AND f.month=7 AND f.day=29 AND f.hour <= 12;

-- Find where the thief escaped to (New York City)
SELECT city
FROM airports
WHERE id = 4;

-- Findn the accomplice (Robin)
SELECT name
FROM people
WHERE phone_number='(375) 555-8161';
