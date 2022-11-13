import {useForm} from 'react-hook-form';
import {EmailRegex} from '../../../const/email-regex';
import {InputData} from '../../forms/types/form-input-props';
import {useRef} from 'react';
import ResumeFormInput from '../../forms/form-inputs/resume-form-input';
import {StyledComponent} from 'styled-components';
import {InputField} from '../../forms/styled/input-field';

export type ResetPasswordFormData = {
  prevPassword: string,
  newPassword: string,
  repeatedPassword: string
}

type ResetPasswordFormProps = {
  submit: (data: ResetPasswordFormData) => void
};

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
      name: 'prev_pass',
      label: '',
      type: 'password',
      options: {
        required: 'Введите свой текущий пароль'
      },
      placeholder: 'Старый пароль'
    },
    {
      name: 'new_pass',
      label: '',
      type: 'password',
      options: {
        required: 'Введите новый пароль'
      },
      placeholder: 'Новый пароль'
    },
    {
      name: 'repeat_pass',
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
    <form onSubmit={handleSubmit(submit)}>
      {
        inputs.map((item, idx) => {
          const ref = item.name === 'new_pass' ? newPassRef : undefined;
          return <ResumeFormInput key={idx} inputRef={ref} errors={errors} register={register} {...item}/>;
        })
      }
    </form>
  );
}
