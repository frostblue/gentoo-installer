from ctypes import ArgumentError


class SFDisk:
    """Utility to help generate sfdisk partition files"""
    
    class Partition:
        def __init__(self, name, device, start, size, bootable):
            self.name = name
            self.device = device
            self.start = start
            self.size = size
            self.bootable = bootable
        
        def dumps(self):
            # probably not the best method but eh https://stackoverflow.com/a/39935542
            type = 7 if self.bootable else 83
            bootstr = ",bootable" if self.bootable else "" 
            sizestr = f",size={self.size}MiB" if self.size > 0 else ""
            return f"{self.device} : start={self.start}MiB{sizestr}{bootstr}\n" # FIXME type= cannot be used since it is not recognized by sfdisk (probably because it doesn't exist on GPT partitions...)

    def __init__(self, label:str, device:str, disksize:str) -> None:
        self.label = label
        self.device = device
        
        self.useddisk = 2 # usually a good idea to leave some space at the start
        self.disksize = disksize
        
        self.partitions = list()
            
    def addpart(self, name:str, size:int=-1, bootable:bool=False, **kwargs) -> str:
        """returns the drive path in dev as a string"""
        leftspace = self.disksize - self.useddisk
        if leftspace < 0:
            raise ArgumentError("Partition is larger than the amount of disk space left")
        
        # if size is not specified use the rest
        # of the disk space by not specifying any size
        rsize = -1
        if size > 0:
            rsize = size
        
        devid = len(self.partitions) + 1
        device = f"{self.device}{devid}"
        newpart = SFDisk.Partition(name, device=device, start=self.useddisk, size=rsize, bootable=bootable)
        self.partitions.append(newpart)
        self.useddisk += rsize
        
        return device
            
    def dumpsconfig(self) -> str:
        configstr = ""
        configstr += f"label: {self.label}\n"
        configstr += f"device: {self.device}\n" # apparently only informative and information is good
        
        configstr += "\n"
        
        for partition in self.partitions:
            configstr += partition.dumps()
        return configstr