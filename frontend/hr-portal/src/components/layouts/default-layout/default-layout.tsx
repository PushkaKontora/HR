import {useSelector} from 'react-redux';
import {Fragment} from 'react';
import styled from 'styled-components';
import {Outlet} from 'react-router-dom';


import Logo from '../../headers/logo/logo';
import Footer from '../../footer/footer';
import {CONTENT_WIDTH} from '../../../const/styled/style-const';
import {useAppSelector} from '../../../app/hooks';
import {UserStatus} from '../../../types/user-status';
import Header from '../../header/header';

const Main = styled.main`
  position: relative;
  width: 100%;
  margin: 0 auto;

  flex-grow: 1;

  height: 100%;
`;

const Page = styled.div`
  overflow: hidden;
  display: flex;
  flex-direction: column;

  min-height: 100vh;
`;

function DefaultLayout() {
  const status = useAppSelector((state) => state.general.statusUser);
  const showFooter = status !== UserStatus.noAuth;

  return (
    <Page>
      <Header/>
      <Main>
        <Outlet/>
      </Main>

      {showFooter && <Footer/>}
    </Page>
  );
}

export default DefaultLayout;
