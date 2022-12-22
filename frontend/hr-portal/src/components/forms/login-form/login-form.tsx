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
import {Navigate, redirect, useLocation, useNavigate} from 'react-router-dom';
import {decodeToken} from '../../../service/token-manager';
import {EMAIL_OPTIONS} from '../../../const/forms/input-options';
import browserHistory from '../../../service/browser-history';
import {AuthRoutes} from '../../../const/app-routes';

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
  const error = useAppSelector((state) => state.general.error);
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      if (userStatus !== UserStatus.noAuth) {
        if (userStatus === UserStatus.user) {
          if (location.state
            && location.state.prevLocation !== '/') {
            navigate(location.state.prevLocation);
          } else {
            navigate(AuthRoutes.Vacancies);
          }
        }
        else if (userStatus === UserStatus.employer) {
          if (location.state) {
            navigate(location.state.prevLocation);
          } else {
            navigate(AuthRoutes.Vacancies);
          }
        }
      }
      /*
      if (userStatus !== UserStatus.noAuth) {
        if (browserHistory.index >= 0) {
          browserHistory.back();
        } else {
          browserHistory.push('/');
        }
      }*/
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
        ...EMAIL_OPTIONS
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
    dispatch(login(data));
    //.then(() => {redirect(location.state.prevLocation);});
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
