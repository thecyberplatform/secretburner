import { computed, ref, Ref } from 'vue';
import {
  useRoute,
  useRouter,
  RouteLocationNormalizedLoaded,
  Router,
} from 'vue-router';
import { useStringUtils } from './useStringUtils';
import { Dialog, Notify } from 'quasar';
import {
  SecretIn,
  SecretOut,
  SecretRetrieveIn,
  SecretRetrieveOut,
} from 'src/types/secret';

import {
  SecretRequestFulfilmentIn,
  SecretRequestFulfilmentRetrievalIn,
  SecretRequestFulfilmentRetrievalOut,
  SecretRequestIn,
  SecretRequestOut,
} from 'src/types/request';

import { ExpiryOption } from 'src/types/generic';

import { useHttpUtils } from './useHttpUtils';
import { useCryptography } from 'src/composables/useCryptography';
import { useBrowserUtils } from 'src/composables/useBrowserUtils';

export const useSecret = () => {
  const disableNewSecret: Ref<boolean> = ref(false);
  const secretText: Ref<string | undefined> = ref();
  const secretLink: Ref<string | undefined> = ref();
  const secretId: Ref<string | undefined> = ref();

  const passphrase: Ref<string | undefined> = ref();
  const confirmPassphrase: Ref<string | undefined> = ref();

  const requestLink: Ref<string | undefined> = ref();
  const requestPublicKey: Ref<string | undefined> = ref();

  const fulfilmentId: Ref<string | undefined> = ref();
  const fulfilmentOk: Ref<boolean> = ref(false);
  const fulfilmentReady: Ref<boolean> = ref(false);

  const burnAt: Ref<number | undefined> = ref();
  const passphraseEncrypted: Ref<boolean> = ref(false);
  const pkiEncrypted: Ref<boolean> = ref(false);

  const { sprintf, deplural, getTextByValue } = useStringUtils();
  const { $t, errorDialogConfig } = useBrowserUtils();

  const resetableFields = {
    secretText,
    secretLink,
    secretId,
    passphrase,
    confirmPassphrase,
    requestLink,
    requestPublicKey,
    fulfilmentId,
    fulfilmentOk,
    fulfilmentReady,
    burnAt,
  };

  const expiry: ExpiryOption[] = [
    { value: 60, text: 'minutes' },
    { value: 3600, text: 'hours' },
    { value: 86400, text: 'days' },
  ];

  const expiryInt: Ref<number> = ref(1);
  const expiryInterval: Ref<number> = ref(86400);

  const { handleFetchResponse, errorMessage, errorStatus } = useHttpUtils();

  const route: RouteLocationNormalizedLoaded = useRoute();
  const router: Router = useRouter();

  const { simpleEncrypt } = useCryptography();

  const { undefinedIfEmpty, updateValueIfTextNotInMatch } = useStringUtils();

  const generateRandomSecret = (): void => {
    const array = new Uint8Array(16);
    window.crypto.getRandomValues(array);

    secretText.value = Array.from(array, (byte) =>
      byte.toString(16).padStart(2, '0')
    ).join('');
  };

  const buildLink = (uuid: string, routeName: string): string => {
    const secretRoute = router.resolve({
      name: routeName,
      params: { uuid },
    });

    return `${window.location.protocol}//${window.location.hostname}${secretRoute.href}`;
  };

  const burnSecret = async (
    passphrase: string | undefined = undefined
  ): Promise<void> => {
    const uuid: string = route.params.uuid?.toString() ?? '';
    const payload: SecretRetrieveIn = {
      secretId: uuid,
      passphrase: passphrase,
    };

    const data: SecretRetrieveOut | null = await handleFetchResponse<
      SecretRetrieveIn,
      SecretRetrieveOut
    >({
      url: '/api/secret/retrieve/',
      method: 'POST',
      json: true,
      body: payload,
    });

    if (data) {
      secretId.value = payload.secretId;
      secretText.value = data.secretText;
      burnAt.value = data.burnAt;
      passphraseEncrypted.value = data.passphraseEncrypted;
      pkiEncrypted.value = data.pkiEncrypted;
    }
  };

  const createSecret = async (
    toEmail?: string,
    fromEmail?: string,
    verifiedToken?: string
  ): Promise<void> => {
    if (!secretText.value) {
      Dialog.create({
        title: $t('Global:Label:ValidationError'),
        message: $t('Global:Validation:SecretLength'),
        ...errorDialogConfig,
      });
      return;
    }

    passphrase.value = undefinedIfEmpty(passphrase.value ?? '');
    if (passphrase.value && secretText.value) {
      secretText.value = await simpleEncrypt(
        secretText.value,
        passphrase.value
      );
    }

    const payload: SecretIn = {
      secretText: secretText.value,
      passphrase: passphrase.value,
      expirySeconds: expiryInt.value * expiryInterval.value,
      toEmail: toEmail,
      fromEmail: fromEmail,
      verifiedToken: verifiedToken,
    };

    const data: SecretOut | null = await handleFetchResponse<
      SecretIn,
      SecretOut
    >({
      url: '/api/secret/',
      method: 'POST',
      json: true,
      body: payload,
    });

    if (data) {
      secretLink.value = buildLink(data.secretId, 'retrieve-secret');
      burnAt.value = data.burnAt;
      resetSecret(['secretLink', 'burnAt']);
      disableNewSecret.value = true;

      if (data.emailResponse && data.emailResponse !== 'ok') {
        Dialog.create({
          message: $t(data.emailResponse),
          ...errorDialogConfig,
        });
      }
    }
  };

  const createSecretRequest = async (
    publicKey?: string,
    verifiedToken?: string,
    toEmail?: string,
    fromEmail?: string
  ): Promise<void> => {
    const payload: SecretRequestIn = {
      passphrase: undefinedIfEmpty(passphrase.value ?? ''),
      expirySeconds: expiryInt.value * expiryInterval.value,
      publicKey: publicKey,
      verifiedToken: verifiedToken,
      toEmail: toEmail,
      fromEmail: fromEmail,
    };

    const data: SecretRequestOut | null = await handleFetchResponse<
      SecretRequestIn,
      SecretRequestOut
    >({
      url: '/api/request/',
      method: 'POST',
      json: true,
      body: payload,
    });

    if (data) {
      secretLink.value = buildLink(data.secretId, 'retrieve-secret');
      requestLink.value = buildLink(data.requestId, 'fulfil-request');

      secretId.value = data.secretId;
      burnAt.value = data.burnAt;

      resetSecret(['secretLink', 'requestLink', 'secretId', 'burnAt']);
    }
  };

  const retrieveRequest = async (): Promise<void> => {
    fulfilmentReady.value = false;

    const uuid: string = route.params.uuid?.toString() ?? '';
    const payload: SecretRequestFulfilmentRetrievalIn = {
      requestId: uuid,
    };

    const data: SecretRequestFulfilmentRetrievalOut | null =
      await handleFetchResponse<
        SecretRequestFulfilmentRetrievalIn,
        SecretRequestFulfilmentRetrievalOut
      >({
        url: '/api/request/retrieve/',
        method: 'POST',
        json: true,
        body: payload,
      });

    if (data) {
      fulfilmentId.value = data.fulfilmentId;
      requestPublicKey.value = undefinedIfEmpty(data.publicKey);

      fulfilmentReady.value = true;
    }
  };

  const fulfilSecretRequest = async (
    verifiedToken?: string,
    toEmail?: string,
    fromEmail?: string
  ): Promise<void> => {
    fulfilmentOk.value = false;

    if (!fulfilmentId.value || !secretText.value) {
      Dialog.create({
        title: $t('Global:Label:ValidationError'),
        message: $t('Global:Validation:FulfilmentRequirement'),
        ...errorDialogConfig,
      });
      return;
    }

    const payload: SecretRequestFulfilmentIn = {
      requestId: route.params.uuid?.toString() ?? '',
      fulfilmentId: fulfilmentId.value,
      secretText: secretText.value,
      verifiedToken: undefinedIfEmpty(verifiedToken ?? ''),
      toEmail: undefinedIfEmpty(toEmail ?? ''),
      fromEmail: undefinedIfEmpty(fromEmail ?? ''),
    };

    if (!fulfilmentId.value) {
      Notify.create({
        message: $t('Global:Validation:FulfilmentNotAuthorised'),
        ...errorDialogConfig,
      });
      return;
    }

    const data: SecretRequestFulfilmentRetrievalOut | null =
      await handleFetchResponse<
        SecretRequestFulfilmentRetrievalIn,
        SecretRequestFulfilmentRetrievalOut
      >({
        url: '/api/request/fulfil/',
        method: 'POST',
        json: true,
        body: payload,
      });

    if (data) {
      resetSecret();
      fulfilmentOk.value = true;
      fulfilmentReady.value = false;
    }
  };

  const resetSecret = (
    excludeFields: (keyof typeof resetableFields)[] = []
  ) => {
    Object.entries(resetableFields).forEach(([field, fieldRef]) => {
      const defaultValue =
        typeof fieldRef.value === 'boolean' ? false : undefined;

      fieldRef.value = updateValueIfTextNotInMatch(
        fieldRef.value,
        field,
        excludeFields as string[],
        defaultValue
      );
    });
  };

  const allowNewSecret = () => {
    resetSecret();
    disableNewSecret.value = false;
  };

  const calculatedSecuritySettingsText = computed(() => {
    const expiryText =
      expiryInt.value.toString() +
      ' ' +
      $t(
        'Global:ExpiryInterval:' +
          deplural(
            getTextByValue(expiryInterval.value, expiry)?.toString() || '',
            expiryInt.value.toString() === '1'
          )
      );

    return sprintf(
      $t('CreateSecret:SecuritySettingsExplanation'),
      passphrase.value ? $t('Global:HasPassphrase') : $t('Global:NoPassphrase'),
      expiryText
    );
  });

  return {
    // functions
    generateRandomSecret,
    createSecretRequest,
    retrieveRequest,
    fulfilSecretRequest,
    createSecret,
    burnSecret,

    // error handling
    errorMessage,
    errorStatus,

    // secret variables
    secretId,
    secretText,
    burnAt,
    passphrase,
    confirmPassphrase,
    requestLink,
    secretLink,
    requestPublicKey,
    fulfilmentId,
    fulfilmentReady,
    fulfilmentOk,
    passphraseEncrypted,
    pkiEncrypted,

    // lookups and local handling
    expiry,
    expiryInt,
    expiryInterval,
    disableNewSecret,
    allowNewSecret,
    resetSecret,
    calculatedSecuritySettingsText,
  };
};
