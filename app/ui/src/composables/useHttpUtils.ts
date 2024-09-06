import { Dialog } from 'quasar';
import ErrorDialog from 'src/components/ErrorDialog.vue';
import { ref, Ref } from 'vue';
import { useStringUtils } from 'src/composables/useStringUtils';

export const useHttpUtils = () => {
  const errorStatus: Ref<string | null> = ref(null);
  const errorMessage: Ref<string | null> = ref(null);
  const errorErrors: Ref<string[] | null> = ref(null);

  const { capitalise } = useStringUtils();

  const handleFetchResponse = async <I, O>(
    options: {
      url: string;
      method: 'POST' | 'GET' | 'PATCH' | 'PUT' | 'HEAD' | 'OPTIONS';
      body?: I;
      json: boolean;
      headers?: HeadersInit;
    },
    errorCallBack?: () => void
  ): Promise<O | null> => {
    errorMessage.value = null;
    errorStatus.value = null;
    errorErrors.value = [];

    const finalHeaders: Record<string, string> = {
      ...(options.headers as Record<string, string>),
    };

    if (options.json) {
      finalHeaders['Content-Type'] = 'application/json';
    }

    try {
      const response = await fetch(options.url, {
        method: options.method,
        body: JSON.stringify(options.body),
        headers: finalHeaders,
      });

      if (!response.ok) {
        const errorData = await response.json();
        errorStatus.value = errorData?.status;
        errorMessage.value = capitalise(errorData?.code);
        errorErrors.value = errorData?.errors;
        throw new Error(errorData);
      }

      return (await response.json()) as O;
    } catch (err) {
      if (errorCallBack) {
        errorCallBack();
      } else {
        Dialog.create({
          component: ErrorDialog,
          componentProps: {
            message: errorMessage.value,
            errors: errorErrors.value,
          },
        });
      }

      return null;
    }
  };

  return {
    handleFetchResponse,
    errorStatus,
    errorMessage,
  };
};
