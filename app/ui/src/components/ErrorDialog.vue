<template>
  <q-dialog ref="dialogRef" @hide="onDialogHide">
    <q-card class="q-dialog-plugin">
      <q-card-section>
        <p class="text-weight-bold">
          {{ message }}
        </p>
        <div v-for="(error, i) in errors" :key="i">{{ error.detail }}</div>
      </q-card-section>
      <q-card-actions class="justify-end">
        <q-btn color="red" label="OK" @click="onOKClick" unelevated />
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script setup lang="ts">
  import { useDialogPluginComponent } from 'quasar';

  interface Error {
    detail: string;
  }

  interface Props {
    message: string;
    errors?: Error[];
  }

  defineProps<Props>();

  defineEmits([...useDialogPluginComponent.emits]);

  const { dialogRef, onDialogHide, onDialogOK } = useDialogPluginComponent();

  function onOKClick() {
    onDialogOK();
  }
</script>
