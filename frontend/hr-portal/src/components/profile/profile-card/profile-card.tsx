import styled from 'styled-components';
import placeholder from '../../../assets/img/profile/placeholder.jpg';
import {XLargeRegular} from '../../styled/fonts/x-large';
import {BlueButton} from '../../styled/buttons/blue-button';
import {User} from '../../../types/user';
import {useEffect, useState} from 'react';
import {ProfileImage} from '../../styled/values/profile-image';
import {getFullName, userStatusToString} from '../../../utils/profile';

const Parent = styled.div`
  width: 710px;
  
  padding: 40px;

  background: #FFFFFF;
  border-radius: 20px;
  
  position: absolute;
  transform: translate(-50%, -50%);
  left: 50%;
  top: 50%;
`;

const Image = styled(ProfileImage)`
  float: left;
  margin-right: 21px;
`;

export type ProfileCardProps = {
  onSettingsClick: () => void
  user: User | null
};

export function ProfileCard({onSettingsClick, user}: ProfileCardProps) {
  const marginBottom12 = {marginBottom: '12px'};

  const [userState, setUserState] = useState(user);

  useEffect(() => {
    setUserState(user);
  }, [user]);

  return (
    <Parent>
      <Image src={userState?.photo || placeholder}/>
      <h4 style={marginBottom12}>{getFullName(userState)}</h4>
      <XLargeRegular>
        <div style={marginBottom12}>{user?.email}</div>
        <div style={marginBottom12}>статус: {userStatusToString(userState)}</div>
      </XLargeRegular>

      <BlueButton as={'button'} onClick={onSettingsClick}>Настройки профиля</BlueButton>
    </Parent>
  );
}
