import { defineAsyncComponent } from 'vue';

const Loading = { template: '<div>Loading...</div>' };
const Failed = { template: '<div>Failed to load module</div>' };

export default [
  {
    path: '/builder',
    component: defineAsyncComponent({
      loader: () => import('builder/App'),
      loadingComponent: Loading,
      errorComponent: Failed,
    }),
  },
  {
    path: '/admin',
    component: defineAsyncComponent({
      loader: () => import('admin/App'),
      loadingComponent: Loading,
      errorComponent: Failed,
    }),
  },
];

