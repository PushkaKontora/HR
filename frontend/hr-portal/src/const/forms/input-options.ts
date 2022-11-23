import {EmailRegex} from '../email-regex';

export const EMAIL_OPTIONS = {
  pattern: {
    value: EmailRegex,
    message: 'Введите корректный e-mail'
  }
};

export const PASSWORD_OPTIONS = {
  minLength: {
    value: 8,
    message: 'Пароль должен содержать не менее 8 символов'
  }
};
