export interface SecretIn {
  secretText: string;
  expirySeconds: number;
  accountId?: string;
  passphrase?: string;
  publicKey?: string;
  toEmail?: string;
  fromEmail?: string;
  verifiedToken?: string;
}

export interface SecretOut {
  secretId: string;
  requestId?: string;
  burnAt: number;
  emailResponse?: string;
}

export interface SecretRetrieveIn {
  secretId: string;
  passphrase?: string;
}

export interface SecretRetrieveOut {
  secretText: string;
  burnAt: number;
  passphraseEncrypted: boolean;
  pkiEncrypted: boolean;
}
