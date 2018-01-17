<?php

require_once('nordeawrapper.php');

$nordeawrapper = new NordeaWrapper();

echo "Get access token:\n";
echo $nordeawrapper->generateAccessToken() . "\n";
echo "\nGet account details:\n";
echo $nordeawrapper->getAccountDetails('FI6593857450293470-EUR') . "\n";
echo "\nGet payments:\n";
echo $nordeawrapper->getPayments() . "\n";
echo "\nGet list of accounts:\n";
echo $nordeawrapper->listAccounts() . "\n";
echo "\nInitiate payment:\n";
echo $nordeawrapper->initiatePayment('FI6593857450293470-EUR', 'FI1350001520000081', '621000.45', 'EUR', 'This is a message, 123!', 'Beneficiary name', 'RF18539007547034') . "\n";
