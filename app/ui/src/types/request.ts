export interface SecretRequestIn {
  expirySeconds?: number;
  passphrase?: string;
  publicKey?: string;
  verifiedToken?: string;
  toEmail?: string;
  fromEmail?: string;
}

export interface SecretRequestOut {
  secretId: string;
  requestId: string;
  burnAt: number;
}

export interface SecretRequestFulfilmentRetrievalIn {
  requestId: string;
}

export interface SecretRequestFulfilmentRetrievalOut {
  requestId: string;
  fulfilmentId: string;
  publicKey: string;
}

export interface SecretRequestFulfilmentIn {
  requestId: string;
  fulfilmentId: string;
  secretText: string;
  verifiedToken?: string;
  toEmail?: string;
  fromEmail?: string;
}

export interface SecretRequestFulfilmentOut {
  requestId: string;
  burnAt: number;
}
