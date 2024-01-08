-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Description of the crime that happened at the given location and time.
SELECT description
  FROM crime_scene_reports
 WHERE year = 2021
   AND month = 7
   AND day = 28
   AND street = 'Humphrey Street';
-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time - each of their interview transcripts mentions the bakery.
-- Littering took place at 16:36. No known witnesses. (Not related info)

-- Finding the names of the witnesses from the interviews table. Also, checking their interviews' transcripts.
SELECT name, transcript
  FROM interviews
 WHERE year = 2021
   AND month = 7
   AND day = 28;

-- The witnesses Ruth, the 2nd Eugene and Raymond had useful info.
-- All three mentioned bakery!

-- Eugene said the thief was withdrawing money from the ATM on Leggett Street.
-- Finding the name of the person who did that transaction.
SELECT name
  FROM people
  JOIN bank_accounts
    ON people.id = bank_accounts.person_id
  JOIN atm_transactions
    ON bank_accounts.account_number = atm_transactions.account_number
 WHERE atm_transactions.year = 2021
   AND atm_transactions.month = 7
   AND atm_transactions.day = 28
   AND atm_transactions.atm_location = 'Leggett Street'
   AND atm_transactions.transaction_type = 'withdraw';


-- Raymond said as the thief was leaving the bakery, they called someone who talked to them for less than a minute. The thief asked the person on the other end of the phone to buy a flight ticket of the earliest flight tomorrow.
-- Info about the aiport in Fiftyville
SELECT full_name, city
  FROM airports
 WHERE city = 'Fiftyville';
-- The name of the airport is Fiftyville Regional Airport.

-- Finding the flights on July 29 from Fiftyville Regional airport.
SELECT flights.id, full_name, city, flights.hour, flights.minute
  FROM airports
  JOIN flights
    ON airports.id = flights.destination_airport_id
 WHERE flights.origin_airport_id =
       (SELECT id
          FROM airports
         WHERE city = 'Fiftyville')
   AND flights.year = 2021
   AND flights.month = 7
   AND flights.day = 29
 ORDER BY flights.hour, flights.minute;
-- First flight is at 8:20 to LaGuardia Airport in New York City.

-- Checking the list of passengers in that flight.
SELECT name
  FROM people
  JOIN passengers
    ON people.passport_number = passengers.passport_number
  JOIN flights
    ON passengers.flight_id = flights.id
 WHERE flights.year = 2021
   AND flights.month = 7
   AND flights.day = 29
   AND flights.hour = 8
   AND flights.minute = 20;

-- Let's check the phone call records.
-- Finding the possible names of the caller.
SELECT name, phone_calls.duration
  FROM people
  JOIN phone_calls
    ON people.phone_number = phone_calls.caller
 WHERE phone_calls.year = 2021
   AND phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60
 ORDER BY phone_calls.duration;

-- Checking the possible names of the call-receiver.
SELECT name, phone_calls.duration
  FROM people
  JOIN phone_calls
    ON people.phone_number = phone_calls.receiver
 WHERE phone_calls.year = 2021
   AND phone_calls.month = 7
   AND phone_calls.day = 28
   AND phone_calls.duration <= 60
   ORDER BY phone_calls.duration;

-- Ruth said the thief drove away in a car from the bakery, within 10 minutes from the theft.
-- checking the license plates of cars and their owners within that 10 minute.
SELECT name, bakery_security_logs.hour, bakery_security_logs.minute
  FROM people
  JOIN bakery_security_logs
    ON people.license_plate = bakery_security_logs.license_plate
 WHERE bakery_security_logs.year = 2021
   AND bakery_security_logs.month = 7
   AND bakery_security_logs.day = 28
   AND bakery_security_logs.activity = 'exit'
   AND bakery_security_logs.hour = 10
   AND bakery_security_logs.minute >= 15
   AND bakery_security_logs.minute <= 25
 ORDER BY bakery_security_logs.minute;

-- It is safe to say that Bruce is the thief! Since his name has appeared in list of who withdrew money from ATM,
-- the list of callers for a duration of less than a minute, the list of passengers of the NY flight,
-- and the list of owners of the license plate numbers seen within ten minutes of theft.

-- and If we match the duration of Bruce's call to the call-reciever, we find his accomplice who is Robin!