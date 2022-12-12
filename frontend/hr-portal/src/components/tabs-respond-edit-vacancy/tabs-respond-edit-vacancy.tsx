import React, {useEffect, useState} from 'react';
import likesIcon from '../../assets/img/vacancy-card/yes_like.svg';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {UserStatus} from '../../types/user-status';
import {
  setIsOpenEditVacancyModal,
  setStateRespondModal,
  setTypeRequestModalVacancy,
  setVacancyByID
} from '../../features/vacancy/vacancy-slice';
import {TypeRequestVacancyModal} from '../../const';
import {LikeButton} from '../../reused-components/like-button/like-button';
import {
  addToVacancyWishlist, deleteFromVacancyWishlist,
  getVacancyWishlist,
  VacancyWishListSortBy
} from '../../service/async-actions/async-actions-vacancy';
import {toast} from 'react-toastify';
import {isFavorite} from '../../utils/favorite';

function TabsRespondEditVacancy() {
  const vacancyByID = useAppSelector((state) => state.vacancy.vacancyByID);
  const favoriteVacancies = useAppSelector((state) => state.user.favoriteVacancies);
  const user = useAppSelector((state) => state.general.user);
  const dispatch = useAppDispatch();

  const handlerClickEditVacancy = (e: any) => {
    dispatch(setVacancyByID(vacancyByID));
    e.stopPropagation();
    dispatch(setTypeRequestModalVacancy(TypeRequestVacancyModal.CHANGE));
    dispatch(setIsOpenEditVacancyModal(true));
  };

  const [liked, setLiked] = useState(Boolean(vacancyByID && isFavorite(vacancyByID, favoriteVacancies)));

  useEffect(() => {
    let mounted = true;

    if (mounted) {
      if (vacancyByID)  {
        setLiked(isFavorite(vacancyByID, favoriteVacancies));
      }
    }

    return () => {
      mounted = false;
    };
  }, [vacancyByID]);

  const handlerClickRespond = (e: any) => {
    dispatch(setVacancyByID(vacancyByID));
    e.stopPropagation();
    dispatch(setStateRespondModal(true));
  };

  const like = () => {
    if (vacancyByID) {
      dispatch(addToVacancyWishlist(vacancyByID.id))
        .then(() => {
          toast.success('Вакансия добавлена в избранное');
          setLiked(true);
          dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));
        });
    }
  };

  const dislike = () => {
    if (vacancyByID) {
      dispatch(deleteFromVacancyWishlist(vacancyByID.id))
        .then(() => {
          toast.error('Вакансия удалена из избранного');
          setLiked(false);
          dispatch(getVacancyWishlist(VacancyWishListSortBy.added_at_desc));
        });
    }
  };

  if (user?.permission === UserStatus.user) {
    return (
      <div className="navTabs">
        <button className="navTabs-btnItem navTabs-btnItem__respond" onClick={handlerClickRespond}>
          Откликнуться
        </button>
        <LikeButton
          onLike={like}
          onDislike={dislike}
          liked={liked}/>
      </div>
    );
  }

  if (user?.permission === UserStatus.employer && vacancyByID !== null) {
    return (
      <>
        {
          vacancyByID.department.id === user?.department.id
            ? (
              <div className="navTabs">
                <button className="navTabs-btnItem navTabs-btnItem__respond" onClick={handlerClickEditVacancy}>
                  Редактировать
                </button>
              </div>)
            : (
              <div className="navTabs">
                <button className="navTabs-btnItem navTabs-btnItem__respond" onClick={handlerClickRespond}>
                  Откликнуться
                </button>
                <LikeButton
                  onLike={like}
                  onDislike={dislike}
                  liked={liked}/>
              </div>
            )
        }
      </>
    );
  }

  return (<></>);
}

export default TabsRespondEditVacancy;