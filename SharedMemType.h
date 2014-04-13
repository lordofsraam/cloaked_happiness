#include <unistd.h>
#include <stdio.h> 
#include <stdlib.h>
#include <iostream>
#include <exception>

#include <sys/ipc.h>
#include <sys/shm.h> 
#include <sys/stat.h>
#include <fcntl.h>

template <class T>
class SharedMemType
{
public:
	SharedMemType (const std::string& keyF, T val = T())
	{
		if (this->FileExists(keyF.c_str()))
		{
			sharedKey = ftok(keyF.c_str(),1);
			if ((sharedSpaceID = shmget(sharedKey, sizeof(T), S_IRUSR | S_IWUSR)) == -1)
				sharedSpaceID = shmget(sharedKey, sizeof(T), IPC_CREAT | S_IRUSR | S_IWUSR);

			value = (T*) shmat(sharedSpaceID, NULL, 0);

			this->setValue(val);
		}
		else
		{
			throw std::exception();
		}
	}

	~SharedMemType ()
	{
		shmdt (value);
	}

	void setValue (const T& val)
	{
		*value = val;
	}

	T getValue ()
	{
		return *value;
	}

	void operator = (const T& val)
	{
		this->setValue(val);
	}

	void Destroy()
	{
		struct shmid_ds shmid;
		shmctl (sharedSpaceID, IPC_RMID, &shmid);
	}
protected:
	bool FileExists (const std::string& name) 
	{
	  struct stat buffer;   
	  return (stat (name.c_str(), &buffer) == 0);
	}
private:
	key_t sharedKey;
	int sharedSpaceID;

	T* value;
};
