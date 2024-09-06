import { LocalStorage, Notify, copyToClipboard } from 'quasar';
import { i18n } from 'boot/i18n';

export const useBrowserUtils = () => {
  const $t = i18n.global.t;

  const successDialogConfig = {
    color: 'teal-9',
    classes: 'text-white',
  };

  const errorDialogConfig = {
    color: 'deep-orange',
    // classes: 'text-white',
  };

  function storeLocally(key: string, value: object | string | number) {
    try {
      LocalStorage.set(key, value);
      Notify.create({
        message: $t('Global:Success:LocalStore'),
        ...successDialogConfig,
      });
    } catch (e) {
      Notify.create({
        message: $t('Global:Error:LocalStore.'),
        ...errorDialogConfig,
      });
    }
  }

  function deleteLocally(key: string) {
    try {
      LocalStorage.removeItem(key);
      Notify.create({
        message: $t('Global:Success:LocalRemoved'),
        ...successDialogConfig,
      });
    } catch (e) {
      Notify.create({
        message: $t('Global:Error:LocalRemoved'),
        ...errorDialogConfig,
      });
    }
  }

  function setClipboard(text: string) {
    copyToClipboard(text)
      .then(() => {
        Notify.create({
          message: $t('Global:Success:Clipboard'),
          ...successDialogConfig,
        });
      })
      .catch(() => {
        Notify.create({
          message: $t('Global:Success:Clipboard'),
          ...errorDialogConfig,
        });
      });
  }

  return {
    storeLocally,
    setClipboard,
    deleteLocally,
    $t,
    successDialogConfig,
    errorDialogConfig,
  };
};
