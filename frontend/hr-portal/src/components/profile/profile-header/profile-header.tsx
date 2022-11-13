import styled from 'styled-components';
import bg from '../../../assets/svg/profile-bg.svg';
import {ProfileCard, ProfileCardProps} from '../profile-card/profile-card';

const Parent = styled.div`
  width: 100%;
  height: 350px;
  
  position: relative;
  background-image: url(${bg});
`;

type ProfileHeaderProps = ProfileCardProps;

export function ProfileHeader(props: ProfileHeaderProps) {
  return (
    <Parent>
      <ProfileCard {...props}/>
    </Parent>
  );
}
