<template>
  <q-card flat bordered class="border-light rounded-5">
    <q-list>
      <q-item
        clickable
        :to="props.to"
        :class="computedClasses"
        class="border-light rounded-5"
      >
        <q-item-section avatar>
          <q-icon
            :name="props.icon"
            size="md"
            :color="props.iconColour ? props.iconColour : ''"
          ></q-icon>
        </q-item-section>
        <q-item-section>
          {{ props.label }}
        </q-item-section>
      </q-item>
    </q-list>
  </q-card>
</template>

<script lang="ts" setup>
  import { computed } from 'vue';
  import { useRoute } from 'vue-router';

  type SBClickCardProps = {
    to: { name: string; params?: unknown };
    label: string;
    icon: string;
    iconColour?: string;
    classes?: string;
    activeClasses?: string;
  };

  const props = defineProps<SBClickCardProps>();
  const route = useRoute();

  const computedClasses = computed(() => {
    let classes = props.classes ? props.classes : undefined;
    if (props.activeClasses && route.name === props.to.name) {
      classes = props.activeClasses;
    }
    return classes;
  });
</script>
