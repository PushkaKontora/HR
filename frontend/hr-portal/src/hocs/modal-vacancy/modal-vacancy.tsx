import React, {ComponentType} from 'react';

type HOCProps = {
  // renderFilmCard: (film: Film) => JSX.Element
}

export const ModalVacancy= (Component: ComponentType) => {
  // class GeneralActionModalVacancy extends React.PureComponent {
  //   constructor(props: any) {
  //     super(props);
  //
  //     this.state = {
  //       nameVacancy: ''
  //     };
  //
  //     this._handleChangeNameVacancy =
  //       this._handleChangeNameVacancy.bind(this);
  //   }
  //
  //   _handleActiveChange() {
  //     this.setState(
  //       (prevState) => ({isActive: !prevState.isActive})
  //     );
  //   }
  //
  //   render() {
  //     return null;
  //   }
  // }

  return <Component />;
};

// function ModalVacancy<T>(Component: ComponentType<T>): ComponentType<Omit<T, keyof HOCProps>> {
//   type ComponentProps = Omit<T, keyof HOCProps>
//
//   function WithFilmCard(props: ComponentProps): JSX.Element {
//     return (
//       <Component
//
//       />
//     );
//   }
//
//   return WithFilmCard;
// }


export default ModalVacancy;