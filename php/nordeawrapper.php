<?php

class NordeaWrapper {
  /**
   * Constants
   */
  private $apiUrl;
  private $clientId;
  private $clientSecret;
  private $redirectUri;
  private $authenticationUrl;
  private $accessTokenUrl;
  private $accountDetailsUrl;
  private $listAccountsUrl;
  private $paymentsUrl;
  private $confirmPaymentSuffix;
  private $configFile;

  /**
   * Variables
   */
  private $accessCode;
  private $accessToken;
  
  public function __construct() {
    $this->configFile = 'config.ini';
    $ini_array = parse_ini_file($this->configFile);
    $this->apiUrl = 'https://api.nordeaopenbanking.com/';
    $this->clientId = $ini_array['clientId'];
    $this->clientSecret = $ini_array['clientSecret'];
    $this->redirectUri = $ini_array['redirectUri'];
    $this->authenticationUrl = $this->apiUrl . 'v1/authentication';
    $this->accessTokenUrl = $this->authenticationUrl . '/access_token';
    $this->accountsUrl = $this->apiUrl . 'v2/accounts';
    $this->paymentsUrl = $this->apiUrl . 'v2/payments/sepa';
    $this->confirmPaymentSuffix = '/confirm';
  }

  private function curlRequest($url, $headers = null, $method = 'get', $payload = null) {
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    if ($headers)
      curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    if ($method == 'post')
      curl_setopt($ch, CURLOPT_POST, true);
    else if ($method == 'put')
      curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
    if ($payload)
      curl_setopt($ch, CURLOPT_POSTFIELDS, $payload);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLINFO_HEADER_OUT, true);
    $body = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    if ((int)($httpCode / 100) != 2)
      return false;

    return $body;
  }
  
  /**
   * Start OAuth authentication by obtaining access code.
   */
  private function getCode() {
    $url = $this->authenticationUrl . '?client_id=' . $this->clientId
      .  '&redirect_uri=' . $this->redirectUri . '&state=';
    
    $response = $this->curlRequest($url);
    $body = substr($response, $curl_info['header_size']);
    
    $this->accessCode = json_decode($body, true)['args']['code'];
  }

  /**
   * Get OAuth access token.
   */
  public function generateAccessToken() {
    if (!isset($this->accessCode))
      $this->getCode();

    $headers = array(
      'Content-Type: application/x-www-form-urlencoded',
      "X-IBM-Client-Id: $this->clientId",
      "X-IBM-Client-Secret: $this->clientSecret"
    );
    $payload = array(
      'code' => $this->accessCode,
      'redirect_uri' => $this->redirectUri
    );
    $payloadQuery = http_build_query($payload);

    $response = $this->curlRequest($this->accessTokenUrl, $headers, 'post', $payloadQuery);
    return $this->accessToken = json_decode($response, true)['access_token'];
  }
  
  public function getAccountDetails($accountId) {
    if (!isset($this->accessToken)) {
      $this->generateAccessToken();
      if (!isset($this->accessToken))
        return false;
    }
    
    $headers = array(
      "X-IBM-Client-Id: $this->clientId",
      "X-IBM-Client-Secret: $this->clientSecret",
      "Authorization: Bearer $this->accessToken"
    );

    $url = $this->accountsUrl . '/' . $accountId;
    return $this->curlRequest($url, $headers);
  }
  
  public function getPayments() {
    if (!isset($this->accessToken)) {
      $this->generateAccessToken();
      if (!isset($this->accessToken))
        return false;
    }
    
    $headers = array(
      "X-IBM-Client-Id: $this->clientId",
      "X-IBM-Client-Secret: $this->clientSecret",
      "Authorization: Bearer $this->accessToken",
      'X-Response-Scenarios: AuthorizationSkipAccessControl',
      'content-type: application/json'
    );

    $url = $this->paymentsUrl . '/';
    return $this->curlRequest($url, $headers);
  }

  public function listAccounts() {
    if (!isset($this->accessToken)) {
      $this->generateAccessToken();
      if (!isset($this->accessToken))
        return false;
    }
    
    $headers = array(
      "X-IBM-Client-Id: $this->clientId",
      "X-IBM-Client-Secret: $this->clientSecret",
      "Authorization: Bearer $this->accessToken"
    );

    return $this->curlRequest($this->accountsUrl, $headers);
  }

  private function getPaymentId($headers, $fromAccount, $toAccount, $amount, $currency, $message, $name, $reference) {
    $payload = array(
      'amount' => $amount,
      'creditor' => array(
        'account' => array('_type' => 'IBAN', 'value' => $toAccount),
        'message' => $message,
        'name' => $name,
        'reference' => array('_type' => 'RF', 'value' => $reference)
      ),
      'currency' => $currency,
      'debtor' => array('_accountId' => $fromAccount)
    );
    
    $payloadJson = json_encode($payload);
    
    $response = $this->curlRequest($this->paymentsUrl, $headers, 'post', $payloadJson);
    return json_decode($response, true)['response']['_id'];
  }
  
  private function confirmPayment($headers, $paymentId) {
    $url = $this->paymentsUrl . '/' . $paymentId . $this->confirmPaymentSuffix;
    return $this->curlRequest($url, $headers, 'put');
  }

  public function initiatePayment($fromAccount, $toAccount, $amount, $currency, $message, $name, $reference) {
    if (!isset($this->accessToken)) {
      $this->generateAccessToken();
      if (!isset($this->accessToken))
        return false;
    }

    $headers = array(
      "X-IBM-Client-Id: $this->clientId",
      "X-IBM-Client-Secret: $this->clientSecret",
      "Authorization: Bearer $this->accessToken",
      'X-Response-Scenarios: AuthorizationSkipAccessControl',
      'Content-Type: application/json'
    );

    $paymentId = $this->getPaymentId($headers, $fromAccount, $toAccount, $amount, $currency, $message, $name, $reference);
    return $this->confirmPayment($headers, $paymentId);
  }
}
