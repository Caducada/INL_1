class Van:
    def __init__(self, name: str) -> None:
        self.name = name
        self.packages = []
        self.gains = []
        self.max_weight = 8000
        self.service_weight = 0
          
    def update_service_weight(self):
        """Uppdaterar vikten för en bil"""
        self.service_weight = 0
        for package in self.packages:
            self.service_weight = self.service_weight + package.weight
             
    def update_gains(self):
        """Uppdaterar värdet på förtjänsten för alla paket"""
        self.gains = []
        for package in self.packages:
            self.gains.append(package.gain)
