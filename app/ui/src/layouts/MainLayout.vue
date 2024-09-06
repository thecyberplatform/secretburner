<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-page class="row flex flex-center">
        <div class="col-xs-12 col-sm-8 col-md-6 col-lg-5 col-xl-3">
          <div class="row justify-evenly q-col-gutter-md q-mb-md">
            <div class="col">
              <SBClickCard
                :to="{ name: 'create-secret' }"
                :label="$t('Global:Label:Create')"
                icon="lock_clock"
                classes="bg-grey-10 text-white"
                active-classes="bg-teal-10 text-white"
              />
            </div>
            <div class="col">
              <SBClickCard
                :to="{ name: 'request-secret' }"
                :label="$t('Global:Label:Request')"
                icon="sync_lock"
                classes="bg-grey-10 text-white"
                active-classes="bg-teal-10 text-white"
              />
            </div>
            <div class="col">
              <SBClickCard
                :to="{ name: 'about' }"
                :label="$t('Global:Label:About')"
                icon="help_center"
                classes="bg-grey-10 text-white"
                active-classes="bg-teal-10 text-white"
              />
            </div>
          </div>
          <router-view />
        </div>
      </q-page>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
  import SBClickCard from 'src/components/SBClickCard.vue';
  import { useBrowserUtils } from 'src/composables/useBrowserUtils';

  defineOptions({
    name: 'MainLayout',
  });

  const { $t } = useBrowserUtils();
</script>

<style lang="sass" scoped></style>
