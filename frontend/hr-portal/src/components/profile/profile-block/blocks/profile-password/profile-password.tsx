import {ProfileBlock, ProfileBlockProps} from '../../profile-block';
import {ResumeTitle} from '../../../../styled/values/resume-title';
import {getDate} from '../../../../../utils/profile';
import {useEffect, useRef, useState} from 'react';
import {User} from '../../../../../types/user';
import {ResetPasswordForm, ResetPasswordFormData} from '../../../reset-password-form/reset-password-form';
import {useAppDispatch} from '../../../../../app/hooks';
import {resetPassword} from '../../../../../service/async-actions/async-actions-user';

type ProfilePasswordProps = {
  user: User | null
}

export function ProfilePassword({user}: ProfilePasswordProps) {
  const [showForm, setShowForm] = useState(false);

  const [userState, setUserState] = useState(user);
  const dispatch = useAppDispatch();

  useEffect(() => {
    setUserState(user);
  }, [user]);

  const handleSubmit = (data: ResetPasswordFormData) => {
    const arg = {
      id: userState?.id,
      previous_password: data.prevPassword,
      new_password: data.newPassword
    };

    //dispatch(resetPassword(arg));
  };

  const input: ProfileBlockProps = {
    title: 'Смена пароля',
    description: 'Выберите надежный пароль и не используйте его для других аккаунтов.',
    buttons: [
      {text: 'Изменить', onClick: () => {return;}},
      {text: 'Сохранить', onClick: () => {return;}},
      {text: 'Отмена', onClick: () => {return;}}
    ],
    children: (
      <div>
        <ResumeTitle>
          Последнее изменение пароля: {getDate(userState?.password.updated_at)}
        </ResumeTitle>
        <div>
          <ResetPasswordForm submit={handleSubmit}/>
        </div>
      </div>
    )
  };

  return (
    <ProfileBlock
      {...input}>
      {input.children}
    </ProfileBlock>
  );
}
