import { RouteRecordRaw } from 'vue-router';

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('layouts/MainLayout.vue'),
    children: [
      {
        path: '',
        name: 'index',
        component: () => import('pages/IndexPage.vue'),
      },
      {
        path: 'about',
        name: 'about',
        component: () => import('pages/AboutPage.vue'),
      },
      {
        path: 'create-secret',
        name: 'create-secret',
        component: () => import('pages/CreateSecretPage.vue'),
      },
      {
        path: 'retrieve-secret/:uuid',
        name: 'retrieve-secret',
        component: () => import('pages/ViewSecretPage.vue'),
      },
      {
        path: 'request-secret',
        name: 'request-secret',
        component: () => import('pages/RequestSecretPage.vue'),
      },
      {
        path: 'fulfil-request/:uuid',
        name: 'fulfil-request',
        component: () => import('pages/FulfilRequestPage.vue'),
      },
      {
        path: 'privacy-policy',
        name: 'privacy-policy',
        component: () => import('pages/PrivacyPolicyPage.vue'),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: '/:catchAll(.*)*',
    component: () => import('pages/ErrorNotFound.vue'),
  },
];

export default routes;
