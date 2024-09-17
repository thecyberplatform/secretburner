<template>
  <div class="row justify-evenly q-col-gutter-md">
    <div class="col">
      <q-card bordered flat>
        <q-card-section class="text-body2">
          <q-markdown>
            {{ $t('PrivacyPolicy:Body') }}
          </q-markdown>
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';

  defineOptions({
    name: 'PrivacyPolicyPage',
  });

  const { $t } = useBrowserUtils();
</script>
