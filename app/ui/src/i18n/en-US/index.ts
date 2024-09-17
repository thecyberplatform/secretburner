export default {
  // Global
  'Global:OhNo': 'Oh No!',
  'Global:PageNotFound': "That page doesn't exist!",
  'Global:OptionalCaption': 'Optional',
  'Global:Hint:PassphraseMismatch': "Passphrases don't match",
  'Global:Hint:PassphraseMatch': 'Both passphrases match!',
  'Global:Placeholder:Secret': 'Enter the secret here...',
  'Global:Placeholder:ConfirmPassphrase': 'Confirm the passphrase',
  'Global:Intro': 'Secure, single-use secrets that vanish after viewing.',

  'Global:Label:Create': 'Create',
  'Global:Label:Request': 'Request',
  'Global:Label:About': 'About',
  'Global:Label:YourEmail': 'Your Email',
  'Global:Label:RecipientEmail': 'Recipient Email',
  'Global:Label:StoreSecret': 'Store the secret',
  'Global:Label:VerifyEmail': 'Verify your email address',
  'Global:Label:SecuritySettings': 'Security settings',
  'Global:Label:Passphrase': 'Passphrase',
  'Global:Label:GetSecret': 'Get secret',
  'Global:Label:CopySecretLink': 'Copy secret link',
  'Global:Label:ValidationError': 'Validation issue',
  'Global:Label:EnableEncryption': 'Enable end-to-end encryption',
  'Global:Label:YourSecret': 'Your secret is...',

  'Global:Validation:VerificationFailed': 'Email verification failed',
  'Global:Validation:FulfilmentRequirement':
    'Must supply a fulfilment code, and secret text.',
  'Global:Validation:FulfilmentNotAuthorised':
    'You are not authorised to fulfil this request',

  'Global:Error:EmailVerification': 'Invalid code or verification ID.',
  'Global:ExpiryInterval:day': 'day',
  'Global:ExpiryInterval:days': 'days',

  'Global:ExpiryInterval:minute': 'minute',
  'Global:ExpiryInterval:minutes': 'minutes',

  'Global:ExpiryInterval:hour': 'hour',
  'Global:ExpiryInterval:hours': 'hours',

  'Global:HasPassphrase': 'has a passphrase',
  'Global:NoPassphrase': 'has no passphrase',

  'Global:Validation:SecretLength': 'Secrets must have at least one character',
  'Global:Validation:VerifyEmail': 'Must supply an email address to verify.',

  'Global:Email:VerifyCode': 'Enter verification Code',
  'Global:Email:Verify': 'Verify',
  'Global:Email:Verified': 'Verified',
  'Global:Email:CheckVerifyEmail':
    'We have sent a verification code to your email address. Please enter it below',

  'Global:EndToEndEncryptedInfo':
    'The plain text of this secret will never touch our servers. You must retrieve your secret using this browser or the secret will be lost forever.',

  'Global:NotEndToEndEncryptedInfo':
    'We will store this secret in plain text until it is retrieved, or expires. After which, it will be irretrievably destroyed.',
  'Global:CopyPrivateKey': 'Copy private key',
  'Global:Label:Delivery': 'Delivery settings',
  'Global:DeliveryInfo': `
  If you want us to send the secret for you, you will need to
  verify yourself first. Fill in the form below and wait
  for your verification code to come via email.`,

  'Global:Success:LocalStore':
    'Data was successfully stored in your local browser storage.',
  'Global:Success:LocalRemoved':
    'Data was successfully removed from your local browser storage.',
  'Global:Success:Clipboard': 'Successfully copied to clipboard',

  'Global:Error:LocalRemoved': 'Error removing locally stored data.',
  'Global:Error:LocalStore':
    'There was an error storing data in your local browser cache.',
  'Global:Error:Clipboard': 'Failed to copy to clipboard',

  // AboutPage.vue
  'AboutPage:Body': `
  ### About SecretBurner

  SecretBurner is a one time secret sharing app.

  ### Features

  Unlike other one time secret apps; SecretBurner has a couple of distinct features:
  1. SecretBurner allows you to "request" a secret from someone.
  2. SecretBurner provides client-side encryption to prevent unencrypted data leaving your browser.
  3. SecretBurner allows you to deliver requests and secrets via email.

  ### Security

  The safest way for a secret to be transmitted is for it to never be sent unencrypted in the first place.

  SecretBurner allows requested secrets to provide a client-side generated key pair, which ensures the secret you request never leaves the browser unencrypted.

  Generating a client-side encryption key pair means the secret can only be read from the same browser you created the request on. You can leave tabs and close the browser, but you must use the same browser.

  SecretBurner also supports simple symmetrical encryption via passphrases. When creating a secret with a passphrase, the
  secret will be encrypted on the client browser and sent to the server fully encrypted.

  When using a passphrase to encrypt a secret, you must ensure delivery of the passphrase to the recipient in order for them
  to retrieve and decrypt the secret.

  Adding a passphrase to a request will only protect its retrieval. If you want the secret to be encrypted when it's fulfilled, you must ensure
  end-to-end encryption is enabled when creating the request.
  `,

  // CreateSecretPage.vue
  'CreateSecret:Title': 'Create Secret',
  'CreateSecret:PassphraseInfo': `
  Adding a passphrase applies AES-256 client side encryption to the secret. The recipient MUST know the passphrase to retrieve the secret.
  `,

  'CreateSecret:EnterSecretPlaceholder': 'Enter secret',
  'CreateSecret:Generate': 'Generate unique secret',
  'CreateSecret:SecretPlaceholder': 'Enter the secret here...',

  'CreateSecret:PassphrasePlaceholder': 'Hard to guess passphrase here',
  'CreateSecret:ExpiryInfo':
    'How long until we burn this secret automatically?',

  'CreateSecret:SecuritySettingsExplanation':
    'This secret %s, and will be destroyed in %s or immediately when retrieved.',
  'CreateSecret:SelfDeliver':
    'You have opted to send this secret to the recipient yourself.',
  'CreateSecret:EmailDelivery': 'We will deliver this secret for you!',
  'CreateSecret:Label:CreateNew': 'New secret',
  'CreateSecret:Label:CreateSecret': 'Create your secret',

  // RequestSecretPage.vue
  'RequestSecret:Title': 'Request a secret from someone',
  'RequestSecret:Body':
    'Use this when you want to keep your secret URL hidden from any form of communication.',
  'RequestSecret:Info:Passphrase':
    'Increase the security of your secret by setting a passphrase to use when you retrieve it.',
  'RequestSecret:Label:EncryptionSettings': 'Encryption Settings',
  'RequestSecret:EncryptionInfo':
    'You can choose to have your secret encrypted end-to-end. Check the box below and a client side key pair will be created specifically for this secret. We will never see the private key, or the secret that ends up being created.',
  'RequestSecret:SuccessfullyCreated':
    "You've successfully created a secret request.",
  'RequestSecret:KeepSecure':
    'Keep the secret link secure! Do not share with anyone',
  'RequestSecret:CopyRequestLink': 'Copy request link',
  'RequestSecret:CopySecretLink': 'Copy secret link',
  'RequestSecret:NewRequest': 'New request',
  'RequestSecret:Label:CreateRequest': 'Create your secret request',

  // FulfilRequestPage.vue
  'FulfilRequest:Title': 'Fulfilling secret request',
  'FulfilRequest:Info': `
    You are fulfilling a secret request.
    This is a ONE-TIME action. If you navigate away from this screen, this request will be burnt, and a new request will need to be created.`,
  'FulfilRequest:Encrypted': `Your secret will be encrypted using the requester's public key
            BEFORE it gets sent to the server. This secret will never been seen
            outside your and the requester's browsers.`,
  'FulfilRequest:NotFound':
    'This request has either been fulfilled or never existed.',
  'FulfilRequest:Successful':
    'The request was successfully fulfilled. The requester will now be able to retrieve the secret.',

  // ViewSecretPage.vue
  'ViewSecret:Title': 'View Secret',
  'ViewSecret:Hint:KnowPassphrase':
    'If you know this secret has a passphrase, enter it here.',
  'ViewSecret:CopySecret': 'Copy to clipboard',
  'ViewSecret:Reveal': 'Reveal secret',
  'ViewSecret:Burnt':
    'This secret has been burnt! Once you leave this page, it is irretrievable.',

  'PrivacyPolicy:Body': `
**Effective date: September 17, 2024**

The short version
- We collect your information only with your consent;
- We only collect the minimum amount of personal information that is necessary to fulfill the purpose of your interaction;
- We never store your personal information; and
- We only use it as this Privacy Statement describes.


### What information we collect and why

Information from website browsers
You do not collect any information from your browser if you simply navigate to our site.

When you use our service (create a secret or request) we record your IP address in a temporary cache.

Why do we collect this?
We collect this information for the purpose of throttling and rate limiting to avoid abuse of our free service.

How we share the information we collect
- We do not share, sell, rent, or trade User Personal Information with third parties for any reason.
- We do not host advertising on secretburner.com
- We do not embed outside content except for Google Fonts.

### Our use of cookies and tracking
#### Cookies
secretburner.com does not use cookies.

#### Third-party tracking services
We do not use tracking services.

### How we secure your information
secretburner.com takes all measures reasonably necessary to protect User Personal Information from unauthorized access, alteration, or destruction; maintain data accuracy; and help ensure the appropriate use of User Personal Information. We follow generally accepted industry standards to protect the personal information submitted to us, both during transmission and once we receive it.

No method of transmission, or method of electronic storage, is 100% secure. Therefore, we cannot guarantee its absolute security. For more information, see our security disclosures.

Our global privacy practices
Information that we collect will be stored and processed in the United States of America in accordance with this Privacy Statement. However, we understand that we have users from different countries and regions with different privacy expectations, and we try to meet those needs.

We may choose to offer data storage in the European Union or other countries in the future. In such circumstances, data entered and stored in the US will not be transferred to the EU or other countries without explicit consent and without changes to this Privacy Statement.

secretburner.com provides clear methods of unambiguous, informed consent at the time of data collection, when we do collect your personal data.
We collect only the minimum amount of personal data necessary, unless you choose to provide more. We encourage you to only give us the amount of data you are comfortable sharing.
We offer you simple methods of accessing, correcting, or deleting the data we have collected.
We provide our users notice, choice, accountability, security, and access, and we limit the purpose for processing. We also provide our users a method of recourse and enforcement. These are the Privacy Shield Principles, but they are also just good practices.
Resolving Complaints
If you have concerns about the way secretburner.com is handling your User Personal Information, please let us know immediately. We want to help. You may email us directly at info@secretburner.com with the subject line "Privacy Concerns." We will respond within 45 days at the latest.

How we respond to compelled disclosure
secretburner.com may disclose personally-identifying information or other information we collect about you to law enforcement in response to a valid subpoena, court order, warrant, or similar government order, or when we believe in good faith that disclosure is reasonably necessary to protect our property or rights, or those of third parties or the public at large.

In complying with court orders and similar legal processes, secretburner.com strives for transparency. When permitted, we will make a reasonable effort to notify users of any disclosure of their information, unless we are prohibited by law or court order from doing so, or in rare, exigent circumstances.

Data Retention and Deletion
Our system is designed to be self-destructive. Any information you share with us will only exist for the length of time you specified when interacting with our service.

How we communicate with you
We don't know who you are. We will never contact you directly unless you have first made contact with us.

Changes to our Privacy Statement
Although most changes are likely to be minor, secretburner.com may change our Privacy Statement from time to time. As we don't know who you are, we encourage you to take not of the effective date, and check this page regularly to see if anything has changed.

Contacting secretburner.com
Questions regarding our Privacy Statement or information practices should be directed to info@secretburner.com.
  `,
};
