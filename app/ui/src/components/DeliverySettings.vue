<template>
  <q-list bordered>
    <q-expansion-item
      dense-toggle
      expand-separator
      icon="send"
      :label="$t('Global:Label:Delivery')"
    >
      <q-card>
        <q-card-section>
          {{ $t('Global:DeliveryInfo') }}
          <div class="row q-col-gutter-md q-mt-md">
            <div class="col">
              <q-input
                v-model="senderEmail"
                outlined
                dense
                :label="$t('Global:Label:YourEmail')"
              />
            </div>
            <div class="col">
              <q-input
                v-model="recipientEmail"
                outlined
                dense
                :label="$t('Global:Label:RecipientEmail')"
              />
            </div>
          </div>
          <div
            class="row q-pt-md q-col-gutter-md"
            v-if="allowVerify && !verifying"
          >
            <div class="col">
              <q-btn
                class="full-width"
                color="teal-9"
                :label="$t('Global:Label:VerifyEmail')"
                unelevated
                no-caps
                @click="createVerificationRequest"
                :loading="loadingRequestVerification"
              ></q-btn>
            </div>
            <div class="col"></div>
          </div>
          <div class="row q-pt-md q-col-gutter-md" v-if="verifying">
            <div class="col text-caption text-weight-bold">
              {{ $t('Global:Email:CheckVerifyEmail') }}
            </div>
          </div>
          <div class="row q-pt-md q-col-gutter-md" v-if="verifying">
            <div class="col flex flex-inline">
              <q-input
                :placeholder="$t('Global:Email:VerifyCode')"
                v-model="verifyCode"
                outlined
                dense
              ></q-input>
              <q-btn
                class="q-ml-md q-px-lg"
                color="teal-9"
                :label="
                  !verifiedOk
                    ? $t('Global:Email:Verify')
                    : $t('Global:Email:Verified')
                "
                unelevated
                no-caps
                @click="submitVerification"
                :loading="loadingVerifyCode"
                :icon="verifiedOk ? 'check' : undefined"
                :disable="verifiedOk"
              ></q-btn>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </q-expansion-item>
  </q-list>
</template>

<script lang="ts" setup>
  import {
    useEmailVerification,
    EmailVerificationEvents,
    IVerifiedEmail,
  } from 'src/composables/useEmailVerification';
  import { i18n } from 'boot/i18n';

  const $t = i18n.global.t;

  const {
    recipientEmail,
    senderEmail,
    createVerifyRequest,
    verifyCode,
    verifyEmailRequest,
    verifying,
    loadingRequestVerification,
    loadingVerifyCode,
    verifiedOk,
    verifiedToken,
    allowVerify,
  } = useEmailVerification();

  interface IProps {
    modelValue: IVerifiedEmail;
  }

  // Define the props
  defineProps<IProps>();

  const emit = defineEmits<EmailVerificationEvents>();

  const submitVerification = async () => {
    await verifyEmailRequest();
    if (verifiedOk.value) {
      emit('update:modelValue', {
        verifiedToken: verifiedToken.value,
        recipientEmail: recipientEmail.value,
        senderEmail: senderEmail.value,
      });
    }
  };

  const createVerificationRequest = async () => {
    await createVerifyRequest();
  };
</script>
