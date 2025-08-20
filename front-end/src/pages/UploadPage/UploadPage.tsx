import { useUploadFile } from "@/api/hooks/uploadFile";
import { useFileExistsQuery } from "@/api/hooks/fileExistsQuery";
import { FileSpreadsheet } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { Spinner } from "./components/Spinner";
import { useEffect, useMemo } from "react";
import { toast } from "sonner";
import { OrganizationDropDown } from "./components/OrganizationDropDown";
import OverwriteModal from "./components/OverwriteModal";
import ConfirmUploadModal from "./components/ConfirmUploadModal";

import { useState } from "react";
import { useGetOrganizationsQuery } from "@/api/hooks/getOrganizationsQuery";

const UploadPage = () => {
  const [selectedOrganisationId, setSelectedOrganization] = useState("");
  const [fileToUpload, setFileToUpload] = useState<File | null>(null);
  const [showOverwriteModal, setShowOverwriteModal] = useState(false);
  const [showConfirmUploadModal, setShowConfirmUploadModal] = useState(false);

  const { mutate: uploadFile, isPending, isSuccess } = useUploadFile();
  const { data: organisations } = useGetOrganizationsQuery();

  const selectedOrganisation = useMemo(
    () => (organisations || []).find(({ id }) => id === selectedOrganisationId),
    [organisations, selectedOrganisationId]
  );
  const {
    data: fileExists,
    isFetching: fetchingFileExists,
    isSuccess: succesFileExists,
  } = useFileExistsQuery({
    filename: fileToUpload?.name ?? "",
    organizationId: selectedOrganisationId,
  });

  const { getRootProps, getInputProps } = useDropzone({
    multiple: false,
    disabled: !selectedOrganisationId,
    accept: {
      "text/csv": [".csv"],
      "application/vnd.ms-excel": [".xls"],
      "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": [
        ".xlsx",
      ],
    },
    onDropAccepted: (files: File[]) => {
      if (!files) return;
      setFileToUpload(files[0]);
    },
    onDropRejected: () => {
      toast.error("Only Excel (.xls, .xlsx) and CSV (.csv) files are allowed.");
    },
  });

  // Show modal if file exists and fileToUpload is set
  useEffect(() => {
    if (fileToUpload && succesFileExists && fileExists) {
      setShowOverwriteModal(true);
    } else if (fileToUpload && succesFileExists && !fileExists) {
      // If file does not exist, show confirm upload modal
      setShowConfirmUploadModal(true);
    }
  }, [
    fileToUpload,
    fileExists,
    selectedOrganisationId,
    uploadFile,
    succesFileExists,
  ]);

  useEffect(() => {
    if (!isPending && isSuccess) {
      toast.success("Successfully uploaded the file");
    }
  }, [isPending, isSuccess]);

  const handleCancel = () => {
    setShowOverwriteModal(false);
    setFileToUpload(null);
  };

  const handleConfirmUploadCancel = () => {
    setShowConfirmUploadModal(false);
    setFileToUpload(null);
  };

  const handleConfirmUpload = () => {
    if (fileToUpload) {
      uploadFile({
        file: fileToUpload,
        organizationId: selectedOrganisationId,
      });
    }
    setShowConfirmUploadModal(false);
    setFileToUpload(null);
  };

  const handleOverwrite = () => {
    if (fileToUpload) {
      uploadFile({
        file: fileToUpload,
        organizationId: selectedOrganisationId,
      });
    }
    setShowOverwriteModal(false);
    setFileToUpload(null);
  };

  return (
    <div className="flex h-full w-full flex-col items-center justify-center p-8 rounded-lg">
      <h2 className="mb-4 text-lg font-semibold text-foreground">
        Upload your file:
      </h2>
      {!isPending && !fetchingFileExists ? (
        <>
          <OrganizationDropDown
            value={selectedOrganisationId}
            onChange={setSelectedOrganization}
          />
          <div
            {...getRootProps({
              className: !selectedOrganisationId
                ? "dropzone disabled cursor-move"
                : "",
            })}
            className={`mt-2 flex flex-col items-center justify-center w-full max-w-lg h-64 border-2 border-dashed border-border rounded-lg bg-background ${
              selectedOrganisationId ? "cursor-pointer" : "cursor-auto"
            } ${
              !!selectedOrganisationId &&
              "hover:bg-accent hover:text-accent-foreground"
            } transition-colors`}
          >
            <input {...getInputProps()} />
            <FileSpreadsheet className="mb-4 h-12 w-12 text-muted-foreground" />
            <p className="text-center text-sm text-muted-foreground">
              Drag & Drop <br /> or{" "}
              <span className="text-primary underline cursor-pointer">
                browse
              </span>
            </p>
          </div>
        </>
      ) : (
        <Spinner />
      )}
      <OverwriteModal
        filename={fileToUpload?.name ?? ""}
        isOpen={showOverwriteModal}
        onCancel={handleCancel}
        onOverwrite={handleOverwrite}
      />
      <ConfirmUploadModal
        filename={fileToUpload?.name ?? ""}
        organisationName={selectedOrganisation?.name ?? ""}
        isOpen={showConfirmUploadModal}
        onCancel={handleConfirmUploadCancel}
        onConfirm={handleConfirmUpload}
      />
    </div>
  );
};

export default UploadPage;
