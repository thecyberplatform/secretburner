<template>
  <div class="row justify-evenly text-center">
    <div class="col">
      <q-card class="bg-transparent text-grey-3">
        <q-card-section>
          {{ $t('Global:Intro') }}
        </q-card-section>
      </q-card>
    </div>
  </div>
</template>

<script setup lang="ts">
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';

  const { $t } = useBrowserUtils();
</script>
