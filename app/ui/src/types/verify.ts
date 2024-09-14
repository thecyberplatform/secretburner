export interface EmailVerifyRequestIn {
  senderEmail: string;
  recipientEmail: string;
}

export interface EmailVerifyRequestOut {
  verifyId: string;
  code: string;
}

export interface VerifyEmailIn {
  verifyId: string;
  code: string;
}

export interface VerifyEmailOut {
  ok: boolean;
  verifiedToken: string;
}
