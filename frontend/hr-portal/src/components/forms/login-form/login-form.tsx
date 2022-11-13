import {useForm} from 'react-hook-form';
import {useEffect, useState} from 'react';
import AuthFormInput from '../form-inputs/auth-form-input';
import {InputData} from '../types/form-input-props';
import {FormSubmit} from '../../styled/forms/form-submit';
import {EmailRegex} from '../../../const/email-regex';
import {LargeRegular} from '../../styled/fonts/large';
import {useAppDispatch, useAppSelector} from '../../../app/hooks';
import {getAuthUser, login} from '../../../service/async-actions/async-actions-user';
import {UserStatus} from '../../../types/user-status';
import {Navigate, redirect, useNavigate} from 'react-router-dom';
import {decodeToken} from '../../../service/token-manager';

type LoginFormData = {
  email: string
  password: string
}

function LoginForm() {
  const {
    register,
    handleSubmit,
    formState: {errors}
  } = useForm<LoginFormData>({
    mode: 'onChange'
  });

  const loading = useAppSelector((state) => state.general.loading);
  const userStatus = useAppSelector((state) => state.general.statusUser);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      if (userStatus !== UserStatus.noAuth) {
        navigate(-1);
      }
    }

    return () => {
      mounted = false;
    };
  }, [userStatus]);


  const inputs: InputData[] = [
    {
      name: 'email',
      label: 'Email',
      type: 'email',
      options: {
        required: 'Вы не ввели e-mail',
        pattern: {
          value: EmailRegex,
          message: 'Введите корректный e-mail'
        }
      }
    },
    {
      name: 'password',
      label: 'Пароль',
      type: 'password',
      options: {
        required: 'Вы не ввели пароль'
      }
    }
  ];

  const onSubmit = (data: LoginFormData) => {
    dispatch(login(data))
      .then(() => {window.location.reload();});
    console.log('Login submitted, awaiting...');
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      {inputs.map((item, idx) => (
        <AuthFormInput key={idx} {...item} errors={errors} register={register}/>
      ))}

      <FormSubmit type='submit' value='Далее' disabled={loading}/>
    </form>
  );
}

export default LoginForm;
