import {useEffect, useLayoutEffect, useRef, useState} from 'react';

import './vacancy-list.scss';
import VacancyCard from '../vacancy-card/vacancy-card';
import Modal from '../../reused-components/modal/modal';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {setStateRespondModal} from '../../features/vacancy/vacancy-slice';
import PaginationCustom from '../pagination-custom/paginationCustom';
import {getVacancies} from '../../service/async-actions/async-actions-vacancy';
import DownLoadIcon from '../../assets/img/job-seach/download.svg';
import EmailPlaneIcon from '../../assets/img/vacancy-card/image_email.png';

function VacancyList() {
  const isOpenRespondModalState = useAppSelector((state) => state.vacancy.isOpenRespondModal);
  //const [isOpenRespondModal, setIsOpenRespondModal] = useState(isOpenRespondModalState);
  const [isOpenRespondModal, setIsOpenRespondModal] = useState(true);
  const [radioChecked, setRadioChecked] = useState(false);
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const vacancies = useAppSelector((state) => state.vacancy.vacancies);
  const vacancyForRespond = useAppSelector((state) => state.vacancy.vacancyByID);
  const user = useAppSelector((state) => state.general.user);
  const resumeUser = useAppSelector((state) => state.user.resumeUser);
  const dispatch = useAppDispatch();
  const firstUpdate = useRef(true);
  const filePicker = useRef<any>(null);

  useLayoutEffect(() => {
    if (firstUpdate.current) {
      firstUpdate.current = false;
      return;
    }
  });

  useEffect(() => {
    dispatch(getVacancies());
    if (user?.resume) {
      const resumeName = resumeUser?.document.split('?')[0].split('/').reverse()[0];
      if (resumeName) {
        setSelectedFile(resumeName);
      }
    }
    console.log('VacancyList');
  }, []);

  useEffect(() => {
    setIsOpenRespondModal(isOpenRespondModalState);
  }, [isOpenRespondModalState]);

  useEffect(() => {
    dispatch(setStateRespondModal(isOpenRespondModal));
  }, [isOpenRespondModal]);

  const onHandlerClickRadio = (e: any) => {
    e.stopPropagation();
    setRadioChecked(!radioChecked);
  };

  const handleSelectNewFileResume = (file: any) => {
    setSelectedFile(file.target.files[0].name);
  };

  const handlePick = () => {
    if (filePicker.current) {
      filePicker.current.click();
    }
  };

  return (
    <>
      <Modal
        padding="80px"
        width={1178}
        active={isOpenRespondModal}
        setActive={setIsOpenRespondModal}
      >
        <div className="respondModalWrapper">
          <div className="respondModalItem respondModalItem__img">
            <img src={EmailPlaneIcon} alt="Email Plane Icon"/>
          </div>
          <div className="respondModalItem respondModalItem__content">
            <div className="title">Отправить отклик на вакансию</div>
            <div className="content">
              <div className="itemContent">
                <div className="titleItem">
                  Вакансия
                </div>
                {vacancyForRespond && (
                  <div className="contentItem">
                    {vacancyForRespond?.name}
                  </div>
                )}
              </div>
              <div className="itemContent">
                <div className="titleItem">
                  Резюме
                </div>

                {selectedFile && (
                  <div className="contentItem">
                    {selectedFile}
                  </div>
                )}

                <div className="contentItem contentItem__image-addNew">
                  <input
                    className="hidden"
                    type="file"
                    onChange={handleSelectNewFileResume}
                    accept="application/pdf"
                    ref={filePicker}
                  />
                  <img src={DownLoadIcon} onClick={handlePick} alt="download icon"/>
                </div>
              </div>
              <div className="itemContent radio-wrapper radio-wrapper__square">
                <input
                  className=" radioInput__square  radioInput__square__after"
                  type="checkbox"
                  name="respond"
                  id="withoutResume"
                  checked={radioChecked}
                  onChange={onHandlerClickRadio}
                />
                <label className="label-radio-input label-radio-input__before" htmlFor="withoutResume">Отправить без резюме</label>
              </div>
            </div>
            <div className="btn-wrapper">
              <button className="btn-sendRespond">Отправить отклик</button>
            </div>
          </div>
        </div>
      </Modal>
      <div className="vacancyListWrapper">
        <div className="vacancyListItem vacancyListItem__list">
          {
            vacancies.items.map((vacancy) => {
              return (<VacancyCard key={vacancy.id} vacancy={vacancy}/>);
            })
          }
        </div>
        <PaginationCustom/>
      </div>
    </>
  );
}

export default VacancyList;

//todo: доделать формат выводимого файла (резюме)