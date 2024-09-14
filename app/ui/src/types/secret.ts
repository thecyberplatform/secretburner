export interface SecretIn {
  secretText: string;
  expirySeconds: number;
  accountId?: string;
  passphrase?: string;
  publicKey?: string;
  recipientEmail?: string;
  senderEmail?: string;
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

export interface SecretRetrieveCheckIn {
  secretId: string;
}

export interface SecretRetrieveCheckOut {
  passphraseProtected: boolean;
}
