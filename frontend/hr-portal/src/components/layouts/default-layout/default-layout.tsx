import {Fragment} from 'react';
import {Outlet} from 'react-router-dom';
import Logo from '../../headers/logo/logo';

function DefaultLayout() {
  return (
    <Fragment>
      <header>
        <Logo></Logo>
      </header>

      <main>
        <Outlet/>
      </main>
    </Fragment>
  );
}

export default DefaultLayout;
