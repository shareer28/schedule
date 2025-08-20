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

interface OverwriteModalProps {
  filename: string;
  isOpen: boolean;
  onCancel: () => void;
  onOverwrite: () => void;
}

const OverwriteModal: React.FC<OverwriteModalProps> = ({
  filename,
  isOpen,
  onCancel,
  onOverwrite,
}) => {
  return (
    <Dialog open={isOpen} onOpenChange={(open) => !open && onCancel()}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>File already exists</DialogTitle>
          <DialogDescription>
            The file <strong>{filename}</strong> already uploaded. Do you want
            to overwrite it?
          </DialogDescription>
        </DialogHeader>
        <DialogFooter>
          <Button variant="outline" onClick={onCancel}>
            Cancel
          </Button>
          <Button variant="destructive" onClick={onOverwrite}>
            Overwrite
          </Button>
        </DialogFooter>
        <DialogClose className="sr-only" />
      </DialogContent>
    </Dialog>
  );
};

export default OverwriteModal;
