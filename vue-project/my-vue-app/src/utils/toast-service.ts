import { useToast } from 'vue-toastification';

const toast = useToast();

export const showErrorToast = (error: string) => {
  toast.error(`エラーが発生しました。詳細: ${error}`, {
    timeout: 5000,
    closeOnClick: true,
    pauseOnHover: true
  });
};

export const showSuccessToast = (message: string) => {
  toast.success(` ${message}:完了`, {
    timeout: 2000,
    closeOnClick: true,
    pauseOnHover: true
  });
};
