<template>
  <div class="row justify-evenly q-col-gutter-md">
    <div class="col">
      <q-card flat bordered class="bg-white text-grey-10">
        <q-card-section class="text-center text-weight-bold"
          >{{ $t('CreateSecret:Title') }}
        </q-card-section>

        <Transition name="slide-up" mode="out-in">
          <div v-if="!disableNewSecret">
            <!-- Secret text area -->
            <q-card-section>
              <q-input
                type="textarea"
                outlined
                v-model="secretText"
                :placeholder="$t('CreateSecret:SecretPlaceholder')"
                dense
              />
              <div class="row">
                <div class="col justify-end flex flex-inline">
                  <q-btn
                    color="grey-3"
                    unelevated
                    @click="generateRandomSecret"
                    class="q-mt-sm text-black"
                    no-caps
                  >
                    {{ $t('CreateSecret:Generate') }}
                  </q-btn>
                </div>
              </div>
            </q-card-section>

            <!-- Security settings area -->
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
                        {{ $t('CreateSecret:PassphraseInfo') }}
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

            <!-- Delivery setting area -->
            <q-card-section>
              <DeliverySettings
                v-model="verifiedEmail"
                :key="verificationKey"
              />
            </q-card-section>

            <!-- Information area -->
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
                        :label="$t('CreateSecret:Label:CreateSecret')"
                        unelevated
                        no-caps
                        @click="submitCreateSecret"
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
            <div class="row justify-evenly">
              <div class="col">
                <div
                  class="row q-col-gutter-md flex items-center justify-center"
                >
                  <div class="col">
                    <q-card flat bordered class="bg-teal-9 text-white">
                      <q-list>
                        <q-item clickable @click="setClipboard(secretLink)">
                          <q-item-section avatar>
                            <q-icon name="content_copy" size="md" />
                          </q-item-section>
                          <q-item-section>
                            {{ $t('Global:Label:CopySecretLink') }}
                          </q-item-section>
                        </q-item>
                      </q-list>
                    </q-card>
                  </div>
                  <div class="col">
                    <q-card flat bordered class="bg-deep-orange text-white">
                      <q-list>
                        <q-item clickable @click="resetSecret">
                          <q-item-section avatar>
                            <q-icon name="add_moderator" size="md" />
                          </q-item-section>
                          <q-item-section>
                            {{ $t('CreateSecret:Label:CreateNew') }}
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
  import { useSecret } from 'src/composables/useSecret';
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';
  import { ref } from 'vue';
  import { IVerifiedEmail } from 'src/composables/useEmailVerification';
  import { Ref } from 'vue/dist/vue';
  import DeliverySettings from 'components/DeliverySettings.vue';

  defineOptions({
    name: 'CreateSecretPage',
  });

  const { setClipboard, $t } = useBrowserUtils();
  const verificationKey: Ref<number> = ref(0);

  const {
    confirmPassphrase,
    disableNewSecret,
    allowNewSecret,
    secretText,
    generateRandomSecret,
    passphrase,
    createSecret,
    expiry,
    expiryInt,
    expiryInterval,
    secretLink,
    calculatedSecuritySettingsText,
  } = useSecret();

  const verifiedEmail: Ref<IVerifiedEmail> = ref({
    recipientEmail: undefined,
    senderEmail: undefined,
    verifiedToken: undefined,
  });

  const resetSecret = () => {
    allowNewSecret();
    verificationKey.value++;
  };

  const submitCreateSecret = () => {
    createSecret(
      verifiedEmail.value.recipientEmail,
      verifiedEmail.value.senderEmail,
      verifiedEmail.value.verifiedToken
    );
  };
</script>
