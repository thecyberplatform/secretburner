<template>
  <div class="row justify-evenly q-col-gutter-md">
    <div class="col">
      <q-card flat bordered class="bg-white text-grey-10">
        <q-card-section class="text-center text-weight-bold"
          >{{ $t('RequestSecret:Title') }}
        </q-card-section>
        <Transition name="slide-up" mode="out-in">
          <div v-if="!requestLink">
            <q-card-section>
              <div class="row">
                <div class="col">
                  <p>
                    {{ $t('RequestSecret:Body') }}
                  </p>
                </div>
              </div>
            </q-card-section>
            <q-card-section>
              <q-list bordered>
                <q-expansion-item
                  dense-toggle
                  expand-separator
                  icon="shield"
                  :label="$t('Global:Label:SecuritySettings')"
                >
                  <q-card>
                    <q-card-section>
                      <p>
                        {{ $t('RequestSecret:Info:Passphrase') }}
                      </p>

                      <div class="row q-col-gutter-md justify-end">
                        <div class="col">
                          <q-input
                            outlined
                            type="password"
                            dense
                            v-model="passphrase"
                            :placeholder="
                              $t('CreateSecret:PassphrasePlaceholder')
                            "
                            bottom-slots
                          >
                            <template #hint>
                              <div
                                class="text-red flex items-center"
                                v-if="
                                  (passphrase && !confirmPassphrase) ||
                                  (confirmPassphrase &&
                                    confirmPassphrase !== passphrase)
                                "
                              >
                                <q-icon
                                  name="warning"
                                  color="yellow-10"
                                  class="q-mr-xs"
                                />
                                {{ $t('Global:Hint:PassphraseMismatch') }}
                              </div>
                              <div
                                class="text-green flex items-center"
                                v-if="
                                  confirmPassphrase &&
                                  confirmPassphrase === passphrase
                                "
                              >
                                <q-icon name="check" class="q-mr-xs" />
                                {{ $t('Global:Hint:PassphraseMatch') }}
                              </div>
                            </template>
                          </q-input>
                        </div>
                        <div class="col">
                          <q-input
                            outlined
                            dense
                            type="password"
                            v-model="confirmPassphrase"
                            :placeholder="
                              $t('Global:Placeholder:ConfirmPassphrase')
                            "
                          ></q-input>
                        </div>
                      </div>
                      <div class="row q-col-gutter-md q-mt-sm">
                        <div class="col text-weight-bold">
                          <p>{{ $t('CreateSecret:ExpiryInfo') }}</p>
                        </div>
                      </div>

                      <div class="row q-col-gutter-md">
                        <div class="col-auto">
                          <q-input
                            type="number"
                            v-model="expiryInt"
                            outlined
                            dense
                            style="max-width: 100px"
                          />
                        </div>
                        <div class="col-auto">
                          <q-select
                            :options="expiry"
                            option-label="text"
                            option-value="value"
                            map-options
                            emit-value
                            v-model="expiryInterval"
                            outlined
                            dense
                          ></q-select>
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>
              </q-list>
            </q-card-section>
            <q-card-section>
              <q-list bordered>
                <q-expansion-item
                  dense-toggle
                  expand-separator
                  icon="password"
                  :label="$t('RequestSecret:Label:EncryptionSettings')"
                >
                  <q-card>
                    <q-card-section>
                      <p>
                        {{ $t('RequestSecret:EncryptionInfo') }}
                      </p>
                      <div class="row q-col-gutter-md q-mt-sm">
                        <div class="col text-right">
                          <q-toggle
                            v-model="usePublicKey"
                            color="teal-9"
                            :label="$t('Global:Label:EnableEncryption')"
                            checked-icon="check"
                            unchecked-icon="clear"
                          />
                        </div>
                      </div>
                    </q-card-section>
                  </q-card>
                </q-expansion-item>
              </q-list>
            </q-card-section>
            <q-card-section>
              <EmailVerification v-model="verifiedEmail" />
            </q-card-section>
            <q-card-section>
              <q-list>
                <q-item>
                  <q-item-section avatar>
                    <q-icon name="warning" color="deep-orange"></q-icon>
                  </q-item-section>
                  <q-item-section class="caption">
                    {{ calculatedSecuritySettingsText }}
                  </q-item-section>
                </q-item>
              </q-list>
              <q-list v-if="usePublicKey">
                <q-item>
                  <q-item-section avatar>
                    <q-icon name="password" color="teal-9"></q-icon>
                  </q-item-section>
                  <q-item-section class="caption">
                    {{ $t('Global:EndToEndEncryptedInfo') }}
                  </q-item-section>
                </q-item>
              </q-list>
              <q-list v-else>
                <q-item>
                  <q-item-section avatar>
                    <q-icon name="abc" color="deep-orange"></q-icon>
                  </q-item-section>
                  <q-item-section class="caption">
                    {{ $t('Global:NotEndToEndEncryptedInfo') }}
                  </q-item-section>
                </q-item>
              </q-list>
              <q-list class="q-mt-sm">
                <q-item v-if="!verifiedEmail.verifiedToken">
                  <q-item-section avatar>
                    <q-icon name="info" color="primary"></q-icon>
                  </q-item-section>
                  <q-item-section class="caption">
                    {{ $t('CreateSecret:SelfDeliver') }}
                  </q-item-section>
                </q-item>
                <q-item v-if="verifiedEmail.verifiedToken">
                  <q-item-section avatar>
                    <q-icon name="check" color="teal-9"></q-icon>
                  </q-item-section>
                  <q-item-section class="caption">
                    {{ $t('CreateSecret:EmailDelivery') }}
                  </q-item-section>
                </q-item>
              </q-list>
            </q-card-section>
            <q-card-section>
              <div class="row justify-evenly">
                <div class="col">
                  <div class="row q-col-gutter-md justify-end">
                    <div class="col">
                      <q-btn
                        class="full-width"
                        color="teal-9"
                        :label="$t('RequestSecret:Label:CreateRequest')"
                        unelevated
                        no-caps
                        @click="createRequest"
                      ></q-btn>
                    </div>
                  </div>
                </div>
              </div>
            </q-card-section>
          </div>
        </Transition>
        <Transition name="slide-up" mode="out-in">
          <q-card-section v-if="secretLink">
            <div class="row justify-evenly" v-if="requestLink && secretLink">
              <div class="col text-center text-subtitle1 text-teal-9">
                {{ $t('RequestSecret:SuccessfullyCreated') }}
                <p class="text-red text-weight-bold">
                  {{ $t('RequestSecret:KeepSecure') }}
                </p>

                <div
                  class="row q-col-gutter-md flex items-center justify-center q-mt-sm"
                >
                  <div class="col">
                    <q-card flat bordered class="bg-teal-9 text-white">
                      <q-list>
                        <q-item
                          clickable
                          @click="setClipboard(requestLink)"
                          class="q-pa-sm"
                        >
                          <q-item-section avatar class="no-min-width">
                            <q-icon name="cloud_upload" size="sm" />
                          </q-item-section>
                          <q-item-section
                            class="text-caption text-body2 text-weight-bold"
                          >
                            {{ $t('RequestSecret:CopyRequestLink') }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-card>
                  </div>
                  <div class="col">
                    <q-card flat bordered class="bg-deep-orange text-white">
                      <q-list>
                        <q-item
                          clickable
                          @click="setClipboard(secretLink)"
                          class="q-pa-sm"
                        >
                          <q-item-section avatar class="no-min-width">
                            <q-icon name="cloud_download" size="sm" />
                          </q-item-section>
                          <q-item-section
                            class="text-caption text-body2 text-weight-bold"
                          >
                            {{ $t('RequestSecret:CopySecretLink') }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-card>
                  </div>
                  <div class="col">
                    <q-card flat bordered class="bg-grey-1">
                      <q-list>
                        <q-item clickable @click="resetRequest" class="q-pa-sm">
                          <q-item-section avatar class="no-min-width">
                            <q-icon name="add_box" size="sm" />
                          </q-item-section>
                          <q-item-section
                            class="text-caption text-body2 text-weight-bold"
                          >
                            {{ $t('RequestSecret:NewRequest') }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-card>
                  </div>
                </div>
              </div>
            </div>
          </q-card-section>
        </Transition>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { Ref, ref, watch } from 'vue';

  import { useSecret } from 'src/composables/useSecret';
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';
  import { useCryptography } from 'src/composables/useCryptography';
  import { IVerifiedEmail } from 'src/composables/useEmailVerification';
  import EmailVerification from 'components/DeliverySettings.vue';

  defineOptions({
    name: 'RequestSecretPage',
  });

  const { $t } = useBrowserUtils();

  const { setClipboard, storeLocally } = useBrowserUtils();

  const verifiedEmail: Ref<IVerifiedEmail> = ref({
    recipientEmail: undefined,
    senderEmail: undefined,
    verifiedToken: undefined,
  });

  const {
    secretLink,
    requestLink,
    passphrase,
    confirmPassphrase,
    createSecretRequest,
    expiry,
    expiryInt,
    expiryInterval,
    secretId,
    burnAt,
    resetSecret,
    calculatedSecuritySettingsText,
  } = useSecret();

  const { generateKeyPair, publicKey, privateKey } = useCryptography();

  const usePublicKey = ref(false);
  const loading = ref(false);

  const exportKeys = async () => {
    loading.value = true;
    await generateKeyPair();
    loading.value = false;
  };

  const createRequest = async () => {
    await createSecretRequest(
      publicKey.value,
      verifiedEmail.value.verifiedToken,
      verifiedEmail.value.recipientEmail,
      verifiedEmail.value.senderEmail
    );
    if (privateKey.value) {
      storeLocally(`sbpvk:${secretId.value}:${burnAt.value}`, privateKey.value);
    }
  };

  const resetRequest = () => {
    usePublicKey.value = false;
    publicKey.value = undefined;
    privateKey.value = undefined;
    resetSecret();
  };

  watch(usePublicKey, (value) => {
    if (value) {
      exportKeys();
    } else {
      publicKey.value = undefined;
      privateKey.value = undefined;
    }
  });
</script>
