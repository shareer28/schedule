import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogFooter,
  DialogTitle,
  DialogDescription,
  DialogClose,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface ConfirmUploadModalProps {
  filename: string;
  organisationName: string;
  isOpen: boolean;
  onCancel: () => void;
  onConfirm: () => void;
}

const ConfirmUploadModal: React.FC<ConfirmUploadModalProps> = ({
  filename,
  organisationName: orginzationName,
  isOpen,
  onCancel,
  onConfirm,
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onCancel()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Confirm Upload</DialogTitle>
          <DialogDescription>
            Are you sure you want to upload the file <strong>{filename}</strong>{" "}
            for organisation <strong>{orginzationName}</strong>?
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button variant="default" onClick={onConfirm}>
            Upload
          </Button>
        </DialogFooter>
        <DialogClose className="sr-only" />
      </DialogContent>
    </Dialog>
  );
};

export default ConfirmUploadModal;
