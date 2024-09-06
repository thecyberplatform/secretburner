<template>
  <div class="row justify-evenly q-col-gutter-md">
    <div class="col">
      <q-card flat bordered class="bg-white text-grey-10">
        <q-card-section class="text-center text-weight-bold"
          >{{ $t('ViewSecret:Title') }}
        </q-card-section>
        <q-card-section>
          <div class="row justify-evenly" v-if="!revealed">
            <div class="col">
              <q-input
                :placeholder="$t('Global:Label:Passphrase')"
                v-model="passphrase"
                :hint="$t('ViewSecret:Hint:KnowPassphrase')"
                dense
                outlined
              ></q-input>
              <q-btn
                :label="$t('Global:Label:GetSecret')"
                no-caps
                unelevated
                color="teal-9"
                @click="callBurnSecret"
                class="q-mt-md"
              ></q-btn>
            </div>
          </div>
          <div class="row justify-evenly" v-if="secretText">
            <div class="col">
              <div class="row q-col-gutter-md flex items-center justify-center">
                <div class="col">
                  <q-card flat bordered class="bg-teal-9 text-white">
                    <q-list>
                      <q-item clickable @click="setClipboard(secretText)">
                        <q-item-section avatar>
                          <q-icon name="content_copy" size="md" />
                        </q-item-section>
                        <q-item-section>
                          {{ $t('ViewSecret:CopySecret') }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-card>
                </div>
                <div class="col">
                  <q-card flat bordered class="bg-deep-orange text-white">
                    <q-list>
                      <q-item clickable @click="revealSecret">
                        <q-item-section avatar>
                          <q-icon name="visibility" size="md" />
                        </q-item-section>
                        <q-item-section>
                          {{ $t('ViewSecret:Reveal') }}
                        </q-item-section>
                      </q-item>
                    </q-list>
                  </q-card>
                </div>
              </div>
            </div>
          </div>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { ref } from 'vue';
  import { useSecret } from 'src/composables/useSecret';
  import { Dialog, LocalStorage } from 'quasar';
  import { useCryptography } from 'src/composables/useCryptography';
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';

  defineOptions({
    name: 'ViewSecretPage',
  });

  const { $t } = useBrowserUtils();

  const passphrase = ref();
  const revealed = ref(false);
  const keyDecrypted = ref(false);

  const { deleteLocally, setClipboard, successDialogConfig } =
    useBrowserUtils();

  const {
    burnSecret,
    secretText,
    secretId,
    burnAt,
    passphraseEncrypted,
    pkiEncrypted,
  } = useSecret();
  const { importPrivateKeyPem, decryptData, simpleDecrypt } = useCryptography();

  const callBurnSecret = async () => {
    await burnSecret(passphrase.value);

    if (secretId.value) {
      const storeKey = `sbpvk:${secretId.value}:${burnAt.value}`;
      const localStoreKey = LocalStorage.getItem(storeKey);

      // Decrypt using the private key stored in the browser.
      if (pkiEncrypted.value && secretText.value) {
        if (localStoreKey && typeof localStoreKey === 'string') {
          const privateKey = await importPrivateKeyPem(localStoreKey);
          secretText.value = await decryptData(privateKey, secretText.value);
          deleteLocally(storeKey);
          keyDecrypted.value = true;
        }
      }

      // Decrypt using the passphrase only.
      if (passphraseEncrypted.value && secretText.value) {
        secretText.value = await simpleDecrypt(
          secretText.value,
          passphrase.value
        );
      }

      revealed.value = true;
    }
  };

  const revealSecret = () => {
    Dialog.create({
      title: $t('Global:Label:YourSecret'),
      message: secretText.value,
      ...successDialogConfig,
    });
  };
</script>
