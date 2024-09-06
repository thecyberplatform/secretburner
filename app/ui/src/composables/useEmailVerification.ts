import { computed, ref, Ref } from 'vue';
import { Dialog } from 'quasar';

import { useHttpUtils } from './useHttpUtils';
import {
  EmailVerifyRequestIn,
  EmailVerifyRequestOut,
  VerifyEmailIn,
  VerifyEmailOut,
} from 'src/types/verify';
import { useStringUtils } from './useStringUtils';
import { useBrowserUtils } from 'src/composables/useBrowserUtils';

export interface IVerifiedEmail {
  verifiedToken?: string;
  toEmail?: string;
  fromEmail?: string;
}

export type EmailVerificationEvents = {
  'update:modelValue': [IVerifiedEmail];
};

export const useEmailVerification = () => {
  const recipientEmail = ref();

  const verifyEmail: Ref<string | undefined> = ref();
  const verifyId: Ref<string | undefined> = ref();
  const verifyCode: Ref<string | undefined> = ref();

  const verifiedOk: Ref<boolean> = ref(false);
  const verifiedToken: Ref<string | undefined> = ref();

  const verifying: Ref<boolean> = ref(false);

  const loadingRequestVerification: Ref<boolean> = ref(false);
  const loadingVerifyCode: Ref<boolean> = ref(false);

  const { handleFetchResponse, errorMessage, errorStatus } = useHttpUtils();
  const { isValidEmail } = useStringUtils();
  const { $t, errorDialogConfig } = useBrowserUtils();

  const createVerifyRequest = async (): Promise<void> => {
    loadingRequestVerification.value = true;
    if (!verifyEmail.value) {
      Dialog.create({
        title: $t('Global:Label:ValidationError'),
        message: $t('Global:Validation:VerifyEmail'),
        ...errorDialogConfig,
      });
      loadingRequestVerification.value = false;

      return;
    }

    const payload: EmailVerifyRequestIn = { toEmail: verifyEmail.value };

    const data: EmailVerifyRequestOut | null = await handleFetchResponse<
      EmailVerifyRequestIn,
      EmailVerifyRequestOut
    >({
      url: '/api/verify/request/',
      method: 'POST',
      json: true,
      body: payload,
    });

    if (data) {
      verifyId.value = data.verifyId;
      verifyCode.value = data.code;
    }
    loadingRequestVerification.value = false;
    verifying.value = true;
  };

  const verifyEmailRequest = async (): Promise<void> => {
    loadingVerifyCode.value = true;

    if (!verifyCode.value || !verifyId.value) {
      Dialog.create({
        title: $t('Global:Validation:VerificationFailed'),
        message: $t('Global:Error:EmailVerification'),
        ...errorDialogConfig,
      });
      loadingVerifyCode.value = false;
      return;
    }

    const payload: VerifyEmailIn = {
      verifyId: verifyId.value,
      code: verifyCode.value,
    };

    const data: VerifyEmailOut | null = await handleFetchResponse<
      VerifyEmailIn,
      VerifyEmailOut
    >(
      {
        url: '/api/verify/',
        method: 'POST',
        json: true,
        body: payload,
      },
      () => {
        Dialog.create({
          title: $t('Global:Validation:VerificationFailed'),
          message: $t('Global:Error:EmailVerification'),
          ...errorDialogConfig,
        });

        verifying.value = false;
        loadingVerifyCode.value = false;
      }
    );

    if (data) {
      verifiedOk.value = data.ok;
      verifiedToken.value = data.verifiedToken;
    }
    loadingVerifyCode.value = false;
  };

  const resetVerification = () => {
    verifyEmail.value = undefined;

    verifyId.value = undefined;
    verifyCode.value = undefined;

    verifiedOk.value = false;
    verifiedToken.value = undefined;

    verifying.value = false;

    loadingRequestVerification.value = false;
    loadingVerifyCode.value = false;
  };

  const allowVerify = computed(() => {
    return !!(
      verifyEmail.value &&
      isValidEmail(verifyEmail.value) &&
      isValidEmail(recipientEmail.value)
    );
  });

  return {
    // error handling
    errorMessage,
    errorStatus,

    // secret variables
    verifyId,
    verifiedToken,
    verifyCode,
    verifyEmail,
    verifiedOk,
    recipientEmail,

    // loading
    loadingRequestVerification,
    loadingVerifyCode,
    verifying,

    // actions
    verifyEmailRequest,
    createVerifyRequest,
    resetVerification,

    // computed
    allowVerify,
  };
};
