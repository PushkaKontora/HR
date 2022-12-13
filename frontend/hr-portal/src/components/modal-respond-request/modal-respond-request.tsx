import Modal from '../../reused-components/modal/modal';
import EmailPlaneIcon from '../../assets/img/vacancy-card/image_email.png';
import DownLoadIcon from '../../assets/img/job-seach/download.svg';
import {useEffect, useRef, useState} from 'react';
import {useAppDispatch, useAppSelector} from '../../app/hooks';
import {postVacancyRequests} from '../../service/async-actions/async-actions-vacancy';
import {setStateRespondModal} from '../../features/vacancy/vacancy-slice';
import {extractFileNameFromYandex} from '../../utils/resume';

function ModalRespondRequest() {
  const isOpenRespondModalState = useAppSelector((state) => state.vacancy.isOpenRespondModal);
  const [isOpenRespondModal, setIsOpenRespondModal] = useState(isOpenRespondModalState);
  const vacancyForRespond = useAppSelector((state) => state.vacancy.vacancyByID);
  const [selectedFileName, setSelectedFileName] = useState<null | string>(null);
  const [selectedFile, setSelectedFile] = useState<null | File>(null);
  const filePicker = useRef<any>(null);
  const [radioChecked, setRadioChecked] = useState(false);
  const resumeUser = useAppSelector((state) => state.user.resumeUser);
  const dispatch = useAppDispatch();
  

  useEffect(() => {
    if (resumeUser) {
      const resumeName = extractFileNameFromYandex(resumeUser?.document);
      if (resumeName) {
        setSelectedFileName(resumeName);
      }
    }
  }, [resumeUser]);

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
    setSelectedFileName(file.target.files[0].name);
    setSelectedFile(file.target.files[0]);
  };

  const handlePick = () => {
    if (filePicker.current) {
      filePicker.current.click();
    }
  };

  const handleRespondRequest = () => {
    if (vacancyForRespond) {
      if (selectedFile) {
        const resumeFile = new FormData();
        resumeFile.append('vacancy_id', vacancyForRespond.id.toString());
        resumeFile.append('resume', selectedFile);
        dispatch(postVacancyRequests(resumeFile));
      } else {
        const resumeFile = new FormData();
        resumeFile.append('vacancy_id', vacancyForRespond.id.toString());
        dispatch(postVacancyRequests(resumeFile));
      }
      setRadioChecked(false);
      setIsOpenRespondModal(false);
    }
  };


  return (
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

              {selectedFileName && (
                <div className="contentItem">
                  {selectedFileName}
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
            <button
              className="btn-sendRespond"
              disabled={!radioChecked && selectedFileName === null}
              onClick={handleRespondRequest}
            >Отправить отклик
            </button>
          </div>
        </div>
      </div>
    </Modal>
  );
}

export default ModalRespondRequest;