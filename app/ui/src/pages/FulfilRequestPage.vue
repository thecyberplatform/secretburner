<template>
  <div class="row justify-evenly q-col-gutter-md">
    <div class="col">
      <q-card flat bordered class="bg-white text-grey-10">
        <q-card-section class="text-center text-weight-bold"
          >{{ $t('FulfilRequest:Title') }}
        </q-card-section>

        <Transition name="slide-up" mode="out-in">
          <div v-if="fulfilmentReady">
            <q-card-section v-if="fulfilmentReady">
              {{ $t('FulfilRequest:Info') }}
            </q-card-section>
            <q-card-section v-if="fulfilmentReady && !fulfilmentOk">
              <q-input
                type="textarea"
                outlined
                v-model="secretText"
                :placeholder="$t('Global:Placeholder:Secret')"
                dense
              />
            </q-card-section>
            <q-card-section v-if="requestPublicKey">
              <q-banner class="bg-red text-white text-weight-bold">
                {{ $t('FulfilRequest:Encrypted') }}
              </q-banner>
            </q-card-section>

            <q-card-section v-if="fulfilmentReady">
              <DeliverySettings v-model="verifiedEmail" />
            </q-card-section>

            <q-card-section v-if="fulfilmentReady">
              <q-btn
                class="full-width"
                color="teal-9"
                :label="$t('Global:Label:StoreSecret')"
                unelevated
                no-caps
                @click="fulfilRequest"
              ></q-btn>
            </q-card-section>
          </div>
        </Transition>

        <Transition name="slide-up" mode="out-in">
          <div v-if="fulfilmentOk">
            <q-card-section v-if="fulfilmentOk">
              <q-banner class="bg-teal-9 text-weight-bold text-white">
                <template v-slot:avatar>
                  <q-icon name="check" color="white" />
                </template>
                {{ $t('FulfilRequest:Successful') }}
              </q-banner>
            </q-card-section>
          </div>
        </Transition>

        <Transition name="slide-up" mode="out-in">
          <q-card-section v-if="!fulfilmentReady && !fulfilmentOk">
            <q-banner class="bg-red text-weight-bold text-white">
              {{ $t('FulfilRequest:NotFound') }}
            </q-banner>
          </q-card-section>
        </Transition>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import DeliverySettings from 'components/DeliverySettings.vue';
  import { useCryptography } from 'src/composables/useCryptography';
  import { IVerifiedEmail } from 'src/composables/useEmailVerification';
  import { useSecret } from 'src/composables/useSecret';
  import { onBeforeMount, ref, Ref } from 'vue';
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';

  defineOptions({
    name: 'FulfilRequestPage',
  });

  const { $t } = useBrowserUtils();

  const {
    secretText,
    retrieveRequest,
    fulfilSecretRequest,
    requestPublicKey,
    fulfilmentReady,
    fulfilmentOk,
  } = useSecret();

  const { encryptData, importPublicKey } = useCryptography();

  onBeforeMount(async () => {
    await retrieveRequest();
  });

  const verifiedEmail: Ref<IVerifiedEmail> = ref({
    recipientEmail: undefined,
    verifiedToken: undefined,
  });

  async function fulfilRequest() {
    if (requestPublicKey.value && secretText.value) {
      const publicKey: CryptoKey = await importPublicKey(
        requestPublicKey.value
      );

      secretText.value = await encryptData(publicKey, secretText.value);
    }

    await fulfilSecretRequest(
      verifiedEmail.value.verifiedToken,
      verifiedEmail.value.toEmail,
      verifiedEmail.value.fromEmail
    );
  }
</script>
