import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {ResumeTitle} from '../../../../styled/resume/resume-title';
import {getDate} from '../../../../../utils/profile';
import {useEffect, useRef, useState} from 'react';
import {User} from '../../../../../types/user';
import {FORM_NAME, ResetPasswordForm, ResetPasswordFormData} from '../../../reset-password-form/reset-password-form';
import {useAppDispatch, useAppSelector} from '../../../../../app/hooks';
import {toast} from 'react-toastify';
import {resetPassword} from '../../../../../service/async-actions/async-actions-profile';

export function ProfilePassword() {
  const [showForm, setShowForm] = useState(false);

  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  const saveRef = useRef<HTMLButtonElement | null>(null);

  const setSaveDisabled = (value: boolean) => {
    if (saveRef.current) {
      saveRef.current.disabled = value;
    }
  };

  const handleSubmit = (data: ResetPasswordFormData) => {
    if (user) {
      const arg = {
        id: user.id,
        previous_password: data.prevPassword,
        new_password: data.newPassword
      };

      setSaveDisabled(true);
      dispatch(resetPassword(arg))
        .then(
          () => {
            //setSaveDisabled(false);
            setShowForm(false);
            toast.success('Пароль успешно изменен');
          },
          () => {setSaveDisabled(false);}
        );
    }
  };

  const input: ProfileBlockProps = {
    title: 'Смена пароля',
    description: 'Выберите надежный пароль и не используйте его для других аккаунтов.',
    buttons: [
      {text: 'Изменить', onClick: () => {setShowForm(true);}, showing: !showForm},
      {text: 'Сохранить', showing: showForm, ref: saveRef, form: FORM_NAME},
      {text: 'Отмена', onClick: () => {setShowForm(false);}, showing: showForm}
    ]
  };

  return (
    <ProfileBlock
      {...input}>
      <div>
        {
          !showForm &&
            <ResumeTitle>
                Последнее изменение пароля: {getDate(user?.password.updated_at)}
            </ResumeTitle>
        }
        {
          showForm &&
            <div>
              <ResetPasswordForm submit={handleSubmit}/>
            </div>
        }
      </div>
    </ProfileBlock>
  );
}
