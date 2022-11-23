import {useForm} from 'react-hook-form';
import {EmailRegex} from '../../../const/email-regex';
import {InputData} from '../../forms/types/form-input-props';
import {useRef} from 'react';
import ResumeFormInput from '../../forms/form-inputs/resume-form-input';
import {StyledComponent} from 'styled-components';
import {InputField} from '../../forms/styled/input-field';
import {PASSWORD_OPTIONS} from '../../../const/forms/input-options';

export type ResetPasswordFormData = {
  prevPassword: string,
  newPassword: string,
  repeatedPassword: string
}

type ResetPasswordFormProps = {
  submit: (data: ResetPasswordFormData) => void
};

export const FORM_NAME = 'RESET_PASSWORD_FORM';
const FIELD_WIDTH = '400px';

export function ResetPasswordForm({submit}: ResetPasswordFormProps) {
  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm<ResetPasswordFormData>({
    mode: 'onChange'
  });

  const newPassRef = useRef<typeof InputField>(null);

  const inputs: InputData[] = [
    {
      name: 'prevPassword',
      label: '',
      type: 'password',
      options: {
        required: 'Введите свой текущий пароль'
      },
      placeholder: 'Старый пароль'
    },
    {
      name: 'newPassword',
      label: '',
      type: 'password',
      options: {
        required: 'Введите новый пароль',
        ...PASSWORD_OPTIONS
      },
      placeholder: 'Новый пароль'
    },
    {
      name: 'repeatedPassword',
      label: '',
      type: 'password',
      options: {
        required: 'Повторите здесь свой новый пароль',
        pattern: {
          value: newPassRef.current?.value,
          message: 'Пароли не совпадают'
        }
      },
      placeholder: 'Повторите новый пароль'
    }
  ];

  return (
    <form id={FORM_NAME} onSubmit={handleSubmit(submit)}>
      {
        inputs.map((item, idx) => {
          const ref = item.name === 'newPassword' ? newPassRef : undefined;
          return <ResumeFormInput width={FIELD_WIDTH} inputMarginBottom={'16px'} key={idx} inputRef={ref} errors={errors} register={register} {...item}/>;
        })
      }
    </form>
  );
}
